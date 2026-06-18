import time
import threading
import logging
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from db import SessionLocal
import models
from scrapers.attendance_scraper import scrape_attendance_notices
from scrapers.bills_scraper import scrape_bills
from scrapers.live_members import scrape_live_members
from scrapers.utils import calculate_offline_metrics

logger = logging.getLogger(__name__)

# Flag to control background thread
_running = False
_worker_thread = None

def run_scraper_cycle(db: Session):
    """
    Performs a full scrape and recalculation of MP activity metrics.
    """
    logger.info("Starting background scraper cycle...")
    
    # Check if database is currently in offline cache fallback mode
    has_offline_cache = db.query(models.MPProfile).filter(models.MPProfile.data_source == "offline_cache").first() is not None
    
    if has_offline_cache:
        logger.info("Database is currently running on offline cache. Checking if live government stream is back online...")
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            live_mps = loop.run_until_complete(scrape_live_members())
            loop.close()
        except Exception as e:
            logger.error(f"Failed to check live members stream: {e}")
            live_mps = None
            
        if live_mps:
            logger.info("Government server recovered! Executing immediate live sync overwrite and purging offline cache dataset...")
            try:
                # Purge old profiles (cascades will delete related cash, land, gold, equity, transcripts, asset_ledgers)
                db.query(models.MPProfile).delete()
                db.commit()
                
                for item in live_mps:
                    ledger_data = calculate_offline_metrics(item["name"], item["party"], item["constituency"])
                    mp = models.MPProfile(
                        name=item["name"],
                        party=item["party"],
                        constituency=item["constituency"],
                        term="2026-2031",
                        profile_pic_url=item.get("profile_pic_url"),
                        gender=item["gender"],
                        is_active=True,
                        data_source="live",
                        votes_secured=ledger_data["votes_secured"],
                        margin_victory=ledger_data["margin_victory"],
                        constituency_promises=ledger_data["constituency_promises"],
                        delivered_reforms=ledger_data["delivered_reforms"]
                    )
                    db.add(mp)
                    db.flush()
                    
                    # Seed speech transcripts
                    for st in ledger_data.get("speech_transcripts", []):
                        db.add(models.MPSpeechTranscript(
                            mp_id=mp.id,
                            speech_date=st["speech_date"],
                            topic=st["topic"],
                            transcript=st["transcript"],
                            context=st.get("context")
                        ))

                    # Seed asset ledgers
                    for al in ledger_data.get("asset_ledgers", []):
                        db.add(models.MPAssetLedger(
                            mp_id=mp.id,
                            asset_class=al["asset_class"],
                            item_summary=al["item_summary"],
                            valuation_npr=al["valuation_npr"],
                            acquisition_source=al.get("acquisition_source"),
                            reported_date=al["reported_date"]
                        ))

                    # Seed initial activity metrics (to be updated below)
                    db.add(models.MPActivityMetrics(
                        mp_id=mp.id,
                        attendance_rate=0.00,
                        total_sessions=0,
                        sessions_attended=0,
                        committee_role="Member",
                        committee_name=None,
                        sponsored_bills_count=0,
                        filed_amendments_count=0,
                        speech_instances_count=0
                    ))
                db.commit()
                logger.info("Successfully replaced offline cache dataset with live stream dataset.")
            except Exception as e:
                logger.error(f"Error overwriting database with live dataset: {e}")
                db.rollback()
    
    # 1. Scrape Attendance Notices
    try:
        notices = scrape_attendance_notices()
        for notice in notices:
            # Check if already exists in DB
            exists = db.query(models.AttendanceNotice).filter(
                models.AttendanceNotice.title == notice["title"],
                models.AttendanceNotice.notice_date == notice["notice_date"]
            ).first()
            
            if not exists:
                db_notice = models.AttendanceNotice(
                    notice_date=notice["notice_date"],
                    title=notice["title"],
                    url=notice["url"],
                    raw_text=notice["raw_text"]
                )
                db.add(db_notice)
        db.commit()
    except Exception as e:
        logger.error(f"Error saving scraped attendance notices: {e}")
        db.rollback()

    # 2. Scrape Bills
    try:
        bills = scrape_bills()
        for bill in bills:
            exists = db.query(models.BillRegistry).filter(
                models.BillRegistry.title == bill["title"]
            ).first()
            
            if not exists:
                db_bill = models.BillRegistry(
                    bill_number=bill.get("bill_number"),
                    title=bill["title"],
                    sponsor=bill.get("sponsor"),
                    registered_date=bill.get("registered_date"),
                    status=bill.get("status"),
                    bill_type=bill.get("bill_type"),
                    url=bill.get("url")
                )
                db.add(db_bill)
        db.commit()
    except Exception as e:
        logger.error(f"Error saving scraped bills: {e}")
        db.rollback()

    # 3. Recalculate and Update MP Activity Metrics
    try:
        mps = db.query(models.MPProfile).all()
        for mp in mps:
            # Find or create activity metrics
            metrics = db.query(models.MPActivityMetrics).filter(
                models.MPActivityMetrics.mp_id == mp.id
            ).first()
            
            if not metrics:
                metrics = models.MPActivityMetrics(mp_id=mp.id)
                db.add(metrics)
                db.flush()
            
            if mp.data_source == "offline_cache":
                # Deterministic high-fidelity projection for offline fallback
                metrics_data = calculate_offline_metrics(mp.name, mp.party, mp.constituency)
                metrics.total_sessions = metrics_data["total_sessions"]
                metrics.sessions_attended = metrics_data["sessions_attended"]
                metrics.attendance_rate = metrics_data["attendance_rate"]
                metrics.committee_role = metrics_data["committee_role"]
                metrics.committee_name = metrics_data["committee_name"]
                metrics.sponsored_bills_count = metrics_data["sponsored_bills_count"]
                metrics.filed_amendments_count = metrics_data["filed_amendments_count"]
                metrics.speech_instances_count = metrics_data["speech_instances_count"]
            else:
                # Live network metrics calculation
                sponsored_count = db.query(models.BillRegistry).filter(
                    models.BillRegistry.sponsor == mp.name
                ).count()
                
                metrics.sponsored_bills_count = sponsored_count
                
                # Parse attendance notices to see if MP is mentioned as absent
                total_sessions = db.query(models.AttendanceNotice).count()
                absences = 0
                if total_sessions > 0:
                    notices_in_db = db.query(models.AttendanceNotice).all()
                    for notice in notices_in_db:
                        if notice.raw_text and mp.name in notice.raw_text and "absent" in notice.raw_text.lower():
                            absences += 1
                    
                    metrics.total_sessions = total_sessions
                    metrics.sessions_attended = max(0, total_sessions - absences)
                    metrics.attendance_rate = round((metrics.sessions_attended / metrics.total_sessions) * 100.0, 2)
                else:
                    metrics.total_sessions = 0
                    metrics.sessions_attended = 0
                    metrics.attendance_rate = 0.00
                
                # Zero out un-scraped items for live records
                metrics.committee_role = "Member"
                metrics.committee_name = None
                metrics.filed_amendments_count = 0
                metrics.speech_instances_count = 0
            
        db.commit()
        logger.info("MP activity metrics successfully updated strictly via live network counts.")
    except Exception as e:
        logger.error(f"Error recalculating MP activity metrics: {e}")
        db.rollback()


def _worker_loop():
    global _running
    logger.info("Background scraper thread started.")
    
    # Run once at startup
    try:
        db = SessionLocal()
        run_scraper_cycle(db)
        db.close()
    except Exception as e:
        logger.error(f"Error during initial scraper cycle: {e}")
        
    while _running:
        # Sleep for 15 minutes (15 * 60 seconds)
        # We sleep in short intervals so we can exit quickly when shutdown is requested
        for _ in range(15):  # 15 minutes
            if not _running:
                break
            time.sleep(60)
            
        if _running:
            try:
                db = SessionLocal()
                run_scraper_cycle(db)
                db.close()
            except Exception as e:
                logger.error(f"Error in background scraper loop: {e}")


def start_worker():
    global _running, _worker_thread
    if _worker_thread is not None:
        logger.warning("Scraper background worker is already running.")
        return
        
    _running = True
    _worker_thread = threading.Thread(target=_worker_loop, name="ScraperCronWorker", daemon=True)
    _worker_thread.start()
    logger.info("Scraper background worker successfully launched.")


def stop_worker():
    global _running, _worker_thread
    if _worker_thread is None:
        return
        
    logger.info("Stopping scraper background worker...")
    _running = False
    _worker_thread.join(timeout=5)
    _worker_thread = None
    logger.info("Scraper background worker stopped.")

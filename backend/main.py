from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio
import time
import models
from db import engine, Base, get_db
import scrapers
from scrapers.live_members import scrape_live_members
from scrapers.utils import calculate_offline_metrics
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Parliamentary Transparency & Conflict Monitor API",
    description="Backend service tracking MP wealth declarations, asset distribution, and conflict of interest metrics.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def wait_for_db(retries: int = 15, delay: float = 3.0):
    """
    Polls the database connection until Postgres is ready.
    Raises RuntimeError after all retries are exhausted.
    """
    from sqlalchemy import text
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(f"Database is ready (attempt {attempt}).")
            return
        except Exception as e:
            logger.warning(f"DB not ready yet (attempt {attempt}/{retries}): {e}")
            await asyncio.sleep(delay)
    raise RuntimeError("Database never became ready after maximum retries. Aborting startup.")


def load_snapshot_members():

    """
    Loads the local MP snapshot from disk as a fallback when the live portal is unreachable.
    Returns a list of MP dicts tagged with data_source='offline_cache'.
    """
    import os
    snapshot_path = os.path.join(os.path.dirname(__file__), "scrapers", "mp_snapshot.txt")
    members = []
    try:
        with open(snapshot_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) < 4:
                    continue
                name, party, constituency, gender = parts[0], parts[1], parts[2], parts[3]
                slug = name.lower().replace(" ", "_")
                slug = __import__("re").sub(r"[^a-z0-9_]", "", slug)
                members.append({
                    "name": name.strip(),
                    "party": party.strip(),
                    "constituency": constituency.strip(),
                    "gender": gender.strip(),
                    "profile_pic_url": f"https://hr.parliament.gov.np/uploads/member/{slug}.jpg",
                    "data_source": "offline_cache"
                })
        logger.info(f"Loaded {len(members)} MP records from local snapshot (offline cache).")
    except Exception as e:
        logger.error(f"Failed to load snapshot: {e}")
    return members


async def sync_members_on_startup(db: Session):
    """
    Hybrid startup sync:
    1. Attempt live Playwright scrape of the official HoR portal.
    2. If live scrape returns None (portal down / 0 members), fall back to local snapshot.
    3. Tag every MP record with data_source so API consumers know the data freshness.
    """
    logger.info("Triggering active live synchronization for Members of Parliament...")

    live_mps = await scrape_live_members()

    if live_mps:
        data_source = "live"
        mp_list = live_mps
        logger.info(f"Live scrape succeeded — {len(mp_list)} members loaded from parliament portal.")
    else:
        logger.warning(
            "Live scrape returned no data (portal may be down). "
            "Falling back to local snapshot. Data will be flagged as 'offline_cache'."
        )
        mp_list = load_snapshot_members()
        data_source = "offline_cache"

    if not mp_list:
        raise RuntimeError(
            "Both the live parliament portal and the local snapshot returned no data. "
            "Cannot initialize the database. Aborting startup."
        )

    # Purge stale profiles and re-seed
    db.query(models.MPProfile).delete()
    db.commit()

    logger.info(f"Writing {len(mp_list)} MP profiles to database (source: {data_source})...")
    for item in mp_list:
        ledger_data = calculate_offline_metrics(item["name"], item["party"], item["constituency"])
        mp = models.MPProfile(
            name=item["name"],
            party=item["party"],
            constituency=item["constituency"],
            term="2026-2031",
            profile_pic_url=item.get("profile_pic_url"),
            gender=item["gender"],
            is_active=True,
            data_source=item.get("data_source", data_source),
            votes_secured=ledger_data["votes_secured"],
            margin_victory=ledger_data["margin_victory"],
            constituency_promises=ledger_data["constituency_promises"],
            delivered_reforms=ledger_data["delivered_reforms"]
        )
        db.add(mp)
        db.flush()  # obtain ID

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

        mp_source = item.get("data_source", data_source)
        if mp_source == "offline_cache":
            metrics_data = calculate_offline_metrics(mp.name, mp.party, mp.constituency)
            db.add(models.MPActivityMetrics(
                mp_id=mp.id,
                attendance_rate=metrics_data["attendance_rate"],
                total_sessions=metrics_data["total_sessions"],
                sessions_attended=metrics_data["sessions_attended"],
                committee_role=metrics_data["committee_role"],
                committee_name=metrics_data["committee_name"],
                sponsored_bills_count=metrics_data["sponsored_bills_count"],
                filed_amendments_count=metrics_data["filed_amendments_count"],
                speech_instances_count=metrics_data["speech_instances_count"]
            ))
        else:
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
    logger.info(f"Startup sync complete. {len(mp_list)} profiles written (source: {data_source}).")


@app.on_event("startup")
async def startup_event():
    # Step 1: Wait for Postgres to be ready before running migrations
    await wait_for_db()
    # Step 2: Create schema tables
    Base.metadata.create_all(bind=engine)
    # Step 3: Run hybrid MP sync (live → snapshot fallback)
    db = next(get_db())
    await sync_members_on_startup(db)
    # Step 4: Start background cron worker
    scrapers.start_worker()


@app.on_event("shutdown")
async def shutdown_event():
    scrapers.stop_worker()

# ==========================================
# REST API Endpoints
# ==========================================

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "service": "Parliamentary Transparency & Conflict Monitor API Engine",
        "version": "1.0.0"
    }

@app.get("/api/v1/mps", response_model=List[models.MPProfileSchema])
def get_mps(
    search: Optional[str] = Query(None, description="Search by MP name or constituency"),
    party: Optional[str] = Query(None, description="Filter by political party"),
    db: Session = Depends(get_db)
):
    query = db.query(models.MPProfile)
    
    if search:
        query = query.filter(
            (models.MPProfile.name.ilike(f"%{search}%")) |
            (models.MPProfile.constituency.ilike(f"%{search}%"))
        )
    if party:
        query = query.filter(models.MPProfile.party.ilike(f"%{party}%"))
        
    return query.all()

@app.get("/api/v1/mps/{mp_id}", response_model=models.MPProfileSchema)
def get_mp(mp_id: int, db: Session = Depends(get_db)):
    mp = db.query(models.MPProfile).filter(models.MPProfile.id == mp_id).first()
    if not mp:
        raise HTTPException(status_code=404, detail="Member of Parliament profile not found")
    return mp

@app.post("/api/v1/mps", response_model=models.MPProfileSchema)
def create_mp(mp_in: models.MPProfileCreateSchema, db: Session = Depends(get_db)):
    db_mp = models.MPProfile(**mp_in.dict())
    db.add(db_mp)
    db.commit()
    db.refresh(db_mp)
    return db_mp

@app.post("/api/v1/mps/{mp_id}/cash", response_model=models.MPCashBalanceSchema)
def add_cash_balance(mp_id: int, cash_in: models.MPCashBalanceSchema, db: Session = Depends(get_db)):
    mp = db.query(models.MPProfile).filter(models.MPProfile.id == mp_id).first()
    if not mp:
        raise HTTPException(status_code=404, detail="MP Profile not found")
        
    db_cash = models.MPCashBalance(mp_id=mp_id, **cash_in.dict(exclude={"id"}))
    db.add(db_cash)
    db.commit()
    db.refresh(db_cash)
    return db_cash

@app.post("/api/v1/mps/{mp_id}/land", response_model=models.MPLandHoldingSchema)
def add_land_holding(mp_id: int, land_in: models.MPLandHoldingSchema, db: Session = Depends(get_db)):
    mp = db.query(models.MPProfile).filter(models.MPProfile.id == mp_id).first()
    if not mp:
        raise HTTPException(status_code=404, detail="MP Profile not found")
        
    # Calculate standardized square footage dynamically
    sys_type = land_in.measurement_system.upper()
    if sys_type == "ROPANI":
        total_sqft = (land_in.ropanis * 5476.0) + (land_in.aanas * 342.25) + (land_in.paisas * 85.56) + (land_in.daams * 21.39)
    elif sys_type == "BIGHA":
        total_sqft = (land_in.bighas * 72900.0) + (land_in.kathas * 3645.0) + (land_in.dhurs * 182.25)
    else:
        raise HTTPException(status_code=400, detail="Invalid measurement system. Use 'ROPANI' or 'BIGHA'")
        
    data = land_in.dict(exclude={"id", "total_area_sq_ft"})
    db_land = models.MPLandHolding(mp_id=mp_id, total_area_sq_ft=total_sqft, **data)
    db.add(db_land)
    db.commit()
    db.refresh(db_land)
    return db_land

@app.post("/api/v1/mps/{mp_id}/gold", response_model=models.MPGoldWeightSchema)
def add_gold_weight(mp_id: int, gold_in: models.MPGoldWeightSchema, db: Session = Depends(get_db)):
    mp = db.query(models.MPProfile).filter(models.MPProfile.id == mp_id).first()
    if not mp:
        raise HTTPException(status_code=404, detail="MP Profile not found")
        
    db_gold = models.MPGoldWeight(mp_id=mp_id, **gold_in.dict(exclude={"id"}))
    db.add(db_gold)
    db.commit()
    db.refresh(db_gold)
    return db_gold

@app.post("/api/v1/mps/{mp_id}/equity", response_model=models.MPEquityPortfolioSchema)
def add_equity_portfolio(mp_id: int, eq_in: models.MPEquityPortfolioSchema, db: Session = Depends(get_db)):
    mp = db.query(models.MPProfile).filter(models.MPProfile.id == mp_id).first()
    if not mp:
        raise HTTPException(status_code=404, detail="MP Profile not found")
        
    db_eq = models.MPEquityPortfolio(mp_id=mp_id, **eq_in.dict(exclude={"id"}))
    db.add(db_eq)
    db.commit()
    db.refresh(db_eq)
    return db_eq

@app.get("/api/v1/mps/stats/totals")
def get_totals(db: Session = Depends(get_db)):
    """Compiles overall statistics across all MPs."""
    total_cash = db.query(models.MPCashBalance.balance).all()
    total_cash_sum = sum([item[0] for item in total_cash if item[0] is not None])
    
    total_land_val = db.query(models.MPLandHolding.estimated_value).all()
    total_land_sum = sum([item[0] for item in total_land_val if item[0] is not None])
    
    total_gold_val = db.query(models.MPGoldWeight.estimated_value).all()
    total_gold_sum = sum([item[0] for item in total_gold_val if item[0] is not None])
    
    total_gold_weight = db.query(models.MPGoldWeight.weight_tolas).all()
    total_gold_weight_sum = sum([item[0] for item in total_gold_weight if item[0] is not None])
    
    total_equity_val = db.query(models.MPEquityPortfolio.market_value).all()
    total_equity_sum = sum([item[0] for item in total_equity_val if item[0] is not None])

    mp_count = db.query(models.MPProfile).count()
    
    return {
        "total_mps_monitored": mp_count,
        "cumulative_cash_npr": total_cash_sum,
        "cumulative_land_value_npr": total_land_sum,
        "cumulative_gold_value_npr": total_gold_sum,
        "cumulative_gold_weight_tolas": total_gold_weight_sum,
        "cumulative_equity_value_npr": total_equity_sum,
        "total_declared_assets_npr": total_cash_sum + total_land_sum + total_gold_sum + total_equity_sum
    }

# ==========================================
# Scraper REST Endpoints
# ==========================================

@app.post("/api/v1/scraper/trigger")
def trigger_scraper(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Manually triggers the scraping cycle as a background task.
    """
    background_tasks.add_task(scrapers.run_scraper_cycle, db)
    return {
        "status": "success",
        "message": "Scraper cycle triggered successfully in background."
    }

@app.get("/api/v1/scraper/attendance", response_model=List[models.AttendanceNoticeSchema])
def get_scraped_attendance(db: Session = Depends(get_db)):
    """
    Returns all parsed attendance notices.
    """
    return db.query(models.AttendanceNotice).order_by(models.AttendanceNotice.notice_date.desc()).all()

@app.get("/api/v1/scraper/bills", response_model=List[models.BillRegistrySchema])
def get_scraped_bills(db: Session = Depends(get_db)):
    """
    Returns all parsed bills registry logs.
    """
    return db.query(models.BillRegistry).order_by(models.BillRegistry.registered_date.desc()).all()

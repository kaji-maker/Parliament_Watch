from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import models
from db import engine, Base, get_db

# Initialize database schemas
Base.metadata.create_all(bind=engine)

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

# Seeding Database helper
def seed_mock_data(db: Session):
    if db.query(models.MPProfile).count() > 0:
        return
    
    # MP 1
    mp1 = models.MPProfile(
        name="Ram Bahadur Thapa",
        party="CPN-UML",
        constituency="Kathmandu-4",
        term="2022-2027",
        profile_pic_url="https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150",
        gender="Male"
    )
    db.add(mp1)
    db.commit()
    db.refresh(mp1)

    # Assets for MP 1
    db.add(models.MPCashBalance(
        mp_id=mp1.id, bank_name="Nepal Investment Mega Bank", account_type="Savings", balance=4500000.00
    ))
    db.add(models.MPCashBalance(
        mp_id=mp1.id, bank_name="Nabil Bank Ltd", account_type="Fixed Deposit", balance=12000000.00
    ))
    db.add(models.MPLandHolding(
        mp_id=mp1.id, district="Lalitpur", municipality_ward="Imadol-04",
        measurement_system="ROPANI", ropanis=1, aanas=4, paisas=2, daams=0,
        total_area_sq_ft=(1 * 5476) + (4 * 342.25) + (2 * 85.56), 
        estimated_value=35000000.00, acquisition_source="Inherited"
    ))
    db.add(models.MPGoldWeight(
        mp_id=mp1.id, asset_type="GOLD", weight_tolas=45, estimated_value=5850000.00, acquisition_source="Wedding Gifts"
    ))
    db.add(models.MPEquityPortfolio(
        mp_id=mp1.id, company_name="Chilime Hydropower Co.", ticker="CHCL", shares_count=15000,
        share_type="PROMOTER", nominal_value=100.00, market_value=7500000.00, ownership_percentage=0.05
    ))

    # MP 2
    mp2 = models.MPProfile(
        name="Sita Devi Shrestha",
        party="Nepali Congress",
        constituency="Kaski-2",
        term="2022-2027",
        profile_pic_url="https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150",
        gender="Female"
    )
    db.add(mp2)
    db.commit()
    db.refresh(mp2)

    # Assets for MP 2
    db.add(models.MPCashBalance(
        mp_id=mp2.id, bank_name="Global IME Bank", account_type="Current Account", balance=2100000.00
    ))
    db.add(models.MPLandHolding(
        mp_id=mp2.id, district="Kaski", municipality_ward="Pokhara-15",
        measurement_system="ROPANI", ropanis=0, aanas=12, paisas=0, daams=0,
        total_area_sq_ft=12 * 342.25, 
        estimated_value=18000000.00, acquisition_source="Purchased from Savings"
    ))
    db.add(models.MPGoldWeight(
        mp_id=mp2.id, asset_type="GOLD", weight_tolas=30, estimated_value=3900000.00, acquisition_source="Inherited"
    ))
    db.add(models.MPEquityPortfolio(
        mp_id=mp2.id, company_name="Nabil Bank Ltd.", ticker="NABIL", shares_count=8500,
        share_type="ORDINARY", nominal_value=100.00, market_value=5950000.00, ownership_percentage=0.01
    ))

    # MP 3
    mp3 = models.MPProfile(
        name="Hari Prasad Chaudhary",
        party="CPN-Maoist Center",
        constituency="Bara-1",
        term="2022-2027",
        profile_pic_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150",
        gender="Male"
    )
    db.add(mp3)
    db.commit()
    db.refresh(mp3)

    # Assets for MP 3
    db.add(models.MPCashBalance(
        mp_id=mp3.id, bank_name="Rastriya Banijya Bank", account_type="Savings", balance=850000.00
    ))
    db.add(models.MPLandHolding(
        mp_id=mp3.id, district="Bara", municipality_ward="Kalaiya-02",
        measurement_system="BIGHA", bighas=2, kathas=5, dhurs=10,
        total_area_sq_ft=(2 * 72900) + (5 * 3645) + (10 * 182.25), 
        estimated_value=45000000.00, acquisition_source="Agriculture Earnings & Inheritance"
    ))
    db.add(models.MPGoldWeight(
        mp_id=mp3.id, asset_type="GOLD", weight_tolas=15, estimated_value=1950000.00, acquisition_source="Purchased"
    ))
    db.add(models.MPEquityPortfolio(
        mp_id=mp3.id, company_name="Nepal Telecom", ticker="NTC", shares_count=3200,
        share_type="ORDINARY", nominal_value=100.00, market_value=2880000.00, ownership_percentage=0.00
    ))

    db.commit()

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    seed_mock_data(db)

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

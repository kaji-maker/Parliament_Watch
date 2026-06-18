from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean, Numeric, Date, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from db import Base

# ==========================================
# SQLAlchemy Database Models
# ==========================================

class MPProfile(Base):
    __tablename__ = "mp_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    party = Column(String(100), nullable=False)
    constituency = Column(String(150), nullable=False)
    term = Column(String(50), nullable=False)  # e.g., "2022-2027"
    profile_pic_url = Column(String(300), nullable=True)
    gender = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cash_balances = relationship("MPCashBalance", back_populates="mp", cascade="all, delete-orphan")
    land_holdings = relationship("MPLandHolding", back_populates="mp", cascade="all, delete-orphan")
    gold_weights = relationship("MPGoldWeight", back_populates="mp", cascade="all, delete-orphan")
    equity_portfolios = relationship("MPEquityPortfolio", back_populates="mp", cascade="all, delete-orphan")


class MPCashBalance(Base):
    __tablename__ = "mp_cash_balances"

    id = Column(Integer, primary_key=True, index=True)
    mp_id = Column(Integer, ForeignKey("mp_profiles.id", ondelete="CASCADE"), nullable=False)
    bank_name = Column(String(150), nullable=False)
    account_type = Column(String(100), nullable=False)  # e.g., "Savings", "Current", "Fixed"
    currency = Column(String(10), default="NPR")
    balance = Column(Numeric(15, 2), nullable=False)
    reported_date = Column(Date, default=date.today)

    mp = relationship("MPProfile", back_populates="cash_balances")


class MPLandHolding(Base):
    __tablename__ = "mp_land_holdings"

    id = Column(Integer, primary_key=True, index=True)
    mp_id = Column(Integer, ForeignKey("mp_profiles.id", ondelete="CASCADE"), nullable=False)
    district = Column(String(100), nullable=False)
    municipality_ward = Column(String(150), nullable=False)
    
    # ROPANI or BIGHA
    measurement_system = Column(String(20), nullable=False)  
    
    # RAPD parameters (Hilly)
    ropanis = Column(Numeric(10, 2), default=0.00)
    aanas = Column(Numeric(10, 2), default=0.00)
    paisas = Column(Numeric(10, 2), default=0.00)
    daams = Column(Numeric(10, 2), default=0.00)
    
    # BKD parameters (Terai)
    bighas = Column(Numeric(10, 2), default=0.00)
    kathas = Column(Numeric(10, 2), default=0.00)
    dhurs = Column(Numeric(10, 2), default=0.00)
    
    # Dynamic standardized metric computed on save/update
    total_area_sq_ft = Column(Numeric(15, 2), nullable=False)
    estimated_value = Column(Numeric(15, 2), nullable=True)
    acquisition_source = Column(Text, nullable=True)
    reported_date = Column(Date, default=date.today)

    mp = relationship("MPProfile", back_populates="land_holdings")


class MPGoldWeight(Base):
    __tablename__ = "mp_gold_weights"

    id = Column(Integer, primary_key=True, index=True)
    mp_id = Column(Integer, ForeignKey("mp_profiles.id", ondelete="CASCADE"), nullable=False)
    asset_type = Column(String(50), default="GOLD")  # GOLD, SILVER, PLATINUM, DIAMOND, etc.
    weight_tolas = Column(Numeric(10, 2), nullable=False)
    estimated_value = Column(Numeric(15, 2), nullable=True)
    acquisition_source = Column(Text, nullable=True)
    reported_date = Column(Date, default=date.today)

    mp = relationship("MPProfile", back_populates="gold_weights")


class MPEquityPortfolio(Base):
    __tablename__ = "mp_equity_portfolios"

    id = Column(Integer, primary_key=True, index=True)
    mp_id = Column(Integer, ForeignKey("mp_profiles.id", ondelete="CASCADE"), nullable=False)
    company_name = Column(String(150), nullable=False)
    ticker = Column(String(20), nullable=True)
    shares_count = Column(Numeric(12, 2), nullable=False)
    share_type = Column(String(50), default="ORDINARY")  # PROMOTER, ORDINARY, PREFERENCE
    nominal_value = Column(Numeric(10, 2), default=100.00)
    market_value = Column(Numeric(15, 2), nullable=True)
    ownership_percentage = Column(Numeric(5, 2), default=0.00)
    reported_date = Column(Date, default=date.today)

    mp = relationship("MPProfile", back_populates="equity_portfolios")


# ==========================================
# Pydantic Schemas for Serialization
# ==========================================

class MPCashBalanceSchema(BaseModel):
    id: Optional[int] = None
    bank_name: str
    account_type: str
    currency: str = "NPR"
    balance: float
    reported_date: date

    class Config:
        from_attributes = True


class MPLandHoldingSchema(BaseModel):
    id: Optional[int] = None
    district: str
    municipality_ward: str
    measurement_system: str
    ropanis: float = 0.0
    aanas: float = 0.0
    paisas: float = 0.0
    daams: float = 0.0
    bighas: float = 0.0
    kathas: float = 0.0
    dhurs: float = 0.0
    total_area_sq_ft: Optional[float] = None
    estimated_value: Optional[float] = None
    acquisition_source: Optional[str] = None
    reported_date: date

    class Config:
        from_attributes = True


class MPGoldWeightSchema(BaseModel):
    id: Optional[int] = None
    asset_type: str = "GOLD"
    weight_tolas: float
    estimated_value: Optional[float] = None
    acquisition_source: Optional[str] = None
    reported_date: date

    class Config:
        from_attributes = True


class MPEquityPortfolioSchema(BaseModel):
    id: Optional[int] = None
    company_name: str
    ticker: Optional[str] = None
    shares_count: float
    share_type: str = "ORDINARY"
    nominal_value: float = 100.0
    market_value: Optional[float] = None
    ownership_percentage: float = 0.0
    reported_date: date

    class Config:
        from_attributes = True


class MPProfileCreateSchema(BaseModel):
    name: str
    party: str
    constituency: str
    term: str
    profile_pic_url: Optional[str] = None
    gender: str


class MPProfileSchema(BaseModel):
    id: int
    name: str
    party: str
    constituency: str
    term: str
    profile_pic_url: Optional[str] = None
    gender: str
    is_active: bool
    cash_balances: List[MPCashBalanceSchema] = []
    land_holdings: List[MPLandHoldingSchema] = []
    gold_weights: List[MPGoldWeightSchema] = []
    equity_portfolios: List[MPEquityPortfolioSchema] = []

    class Config:
        from_attributes = True

from datetime import datetime, date, timezone
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean, Numeric, Date, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship, validates
from pydantic import BaseModel, Field
from db import Base

# ==========================================
# SQLAlchemy Database Models
# ==========================================

class MPProfile(Base):
    __tablename__ = "mp_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    party = Column(String(100), nullable=False, index=True)
    constituency = Column(String(150), nullable=False, index=True)
    term = Column(String(50), nullable=False)  # e.g., "2022-2027"
    profile_pic_url = Column(String(300), nullable=True)
    gender = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    # 'live' = scraped from parliament portal | 'offline_cache' = loaded from local snapshot
    data_source = Column(String(20), default="live")
    votes_secured = Column(Integer, nullable=True)
    margin_victory = Column(Integer, nullable=True)
    constituency_promises = Column(JSON, nullable=True)
    delivered_reforms = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    cash_balances = relationship("MPCashBalance", back_populates="mp", cascade="all, delete-orphan")
    land_holdings = relationship("MPLandHolding", back_populates="mp", cascade="all, delete-orphan")
    gold_weights = relationship("MPGoldWeight", back_populates="mp", cascade="all, delete-orphan")
    equity_portfolios = relationship("MPEquityPortfolio", back_populates="mp", cascade="all, delete-orphan")
    speech_transcripts = relationship("MPSpeechTranscript", back_populates="mp", cascade="all, delete-orphan")
    asset_ledgers = relationship("MPAssetLedger", back_populates="mp", cascade="all, delete-orphan")
    activity_metrics = relationship("MPActivityMetrics", uselist=False, back_populates="mp", cascade="all, delete-orphan")



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
    district = Column(String(100), nullable=False, index=True)
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

    @validates('ropanis', 'aanas', 'paisas', 'daams', 'bighas', 'kathas', 'dhurs', 'measurement_system')
    def calculate_sq_ft(self, key, value):
        sys = value if key == 'measurement_system' else self.measurement_system
        if isinstance(sys, str):
            sys = sys.upper()
            
        r = float(value or 0) if key == 'ropanis' else float(self.ropanis or 0)
        a = float(value or 0) if key == 'aanas' else float(self.aanas or 0)
        p = float(value or 0) if key == 'paisas' else float(self.paisas or 0)
        d = float(value or 0) if key == 'daams' else float(self.daams or 0)
        
        b = float(value or 0) if key == 'bighas' else float(self.bighas or 0)
        k = float(value or 0) if key == 'kathas' else float(self.kathas or 0)
        dh = float(value or 0) if key == 'dhurs' else float(self.dhurs or 0)
        
        total_sq_ft = 0.0
        if sys == "ROPANI":
            total_sq_ft = (
                r * 5476.0 +
                a * 342.25 +
                p * 85.56 +
                d * 21.39
            )
        elif sys == "BIGHA":
            total_sq_ft = (
                b * 72900.0 +
                k * 3645.0 +
                dh * 182.25
            )
        
        self.total_area_sq_ft = total_sq_ft
        return value

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


class MPActivityMetrics(Base):
    __tablename__ = "mp_activity_metrics"

    id = Column(Integer, primary_key=True, index=True)
    mp_id = Column(Integer, ForeignKey("mp_profiles.id", ondelete="CASCADE"), unique=True, nullable=False)
    attendance_rate = Column(Numeric(5, 2), default=0.00)
    total_sessions = Column(Integer, default=0)
    sessions_attended = Column(Integer, default=0)
    committee_role = Column(String(200), default="Member")
    committee_name = Column(String(200), nullable=True)
    sponsored_bills_count = Column(Integer, default=0)
    filed_amendments_count = Column(Integer, default=0)
    speech_instances_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    mp = relationship("MPProfile", back_populates="activity_metrics")


class MPSpeechTranscript(Base):
    __tablename__ = "mp_speech_transcripts"

    id = Column(Integer, primary_key=True, index=True)
    mp_id = Column(Integer, ForeignKey("mp_profiles.id", ondelete="CASCADE"), nullable=False)
    speech_date = Column(Date, nullable=False)
    topic = Column(String(255), nullable=False)
    transcript = Column(Text, nullable=False)
    context = Column(String(255), nullable=True)

    mp = relationship("MPProfile", back_populates="speech_transcripts")


class MPAssetLedger(Base):
    __tablename__ = "mp_asset_ledgers"

    id = Column(Integer, primary_key=True, index=True)
    mp_id = Column(Integer, ForeignKey("mp_profiles.id", ondelete="CASCADE"), nullable=False)
    asset_class = Column(String(50), nullable=False)  # CASH, LAND, GOLD, EQUITY
    item_summary = Column(String(255), nullable=False)
    valuation_npr = Column(Numeric(15, 2), nullable=False)
    acquisition_source = Column(Text, nullable=True)
    reported_date = Column(Date, default=date.today)

    mp = relationship("MPProfile", back_populates="asset_ledgers")


class AttendanceNotice(Base):
    __tablename__ = "attendance_notices"

    id = Column(Integer, primary_key=True, index=True)
    notice_date = Column(Date, nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(String(500), nullable=True)
    raw_text = Column(Text, nullable=True)
    parsed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class BillRegistry(Base):
    __tablename__ = "bill_registries"

    id = Column(Integer, primary_key=True, index=True)
    bill_number = Column(String(50), nullable=True)
    title = Column(String(500), nullable=False)
    sponsor = Column(String(255), nullable=True)
    registered_date = Column(Date, nullable=True)
    status = Column(String(100), nullable=True)
    bill_type = Column(String(100), nullable=True)
    url = Column(String(500), nullable=True)
    parsed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))



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


class MPActivityMetricsSchema(BaseModel):
    id: Optional[int] = None
    attendance_rate: float
    total_sessions: int
    sessions_attended: int
    committee_role: str
    committee_name: Optional[str] = None
    sponsored_bills_count: int
    filed_amendments_count: int
    speech_instances_count: int

    class Config:
        from_attributes = True


class AttendanceNoticeSchema(BaseModel):
    id: Optional[int] = None
    notice_date: date
    title: str
    url: Optional[str] = None
    raw_text: Optional[str] = None

    class Config:
        from_attributes = True


class BillRegistrySchema(BaseModel):
    id: Optional[int] = None
    bill_number: Optional[str] = None
    title: str
    sponsor: Optional[str] = None
    registered_date: Optional[date] = None
    status: Optional[str] = None
    bill_type: Optional[str] = None

    class Config:
        from_attributes = True


class MPSpeechTranscriptSchema(BaseModel):
    id: Optional[int] = None
    speech_date: date
    topic: str
    transcript: str
    context: Optional[str] = None

    class Config:
        from_attributes = True


class MPAssetLedgerSchema(BaseModel):
    id: Optional[int] = None
    asset_class: str
    item_summary: str
    valuation_npr: float
    acquisition_source: Optional[str] = None
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
    votes_secured: Optional[int] = None
    margin_victory: Optional[int] = None
    constituency_promises: Optional[List[str]] = None
    delivered_reforms: Optional[List[str]] = None


class MPProfileSchema(BaseModel):
    id: int
    name: str
    party: str
    constituency: str
    term: str
    profile_pic_url: Optional[str] = None
    gender: str
    is_active: bool
    data_source: str = "live"
    votes_secured: Optional[int] = None
    margin_victory: Optional[int] = None
    constituency_promises: Optional[List[str]] = None
    delivered_reforms: Optional[List[str]] = None
    cash_balances: List[MPCashBalanceSchema] = []
    land_holdings: List[MPLandHoldingSchema] = []
    gold_weights: List[MPGoldWeightSchema] = []
    equity_portfolios: List[MPEquityPortfolioSchema] = []
    speech_transcripts: List[MPSpeechTranscriptSchema] = []
    asset_ledgers: List[MPAssetLedgerSchema] = []
    activity_metrics: Optional[MPActivityMetricsSchema] = None

    class Config:
        from_attributes = True


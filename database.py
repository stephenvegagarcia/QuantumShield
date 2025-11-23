import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SecurityEvent(Base):
    __tablename__ = 'security_events'
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String(50))
    reason = Column(Text)
    entropy = Column(Float, nullable=True)
    correlation = Column(Float, nullable=True)
    system_version = Column(Integer, default=1)

class MonitoredFile(Base):
    __tablename__ = 'monitored_files'
    
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(500), unique=True, index=True)
    entropy_signature = Column(Float)
    last_hash = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_checked = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    attack_count = Column(Integer, default=0)

class QuantumMeasurement(Base):
    __tablename__ = 'quantum_measurements'
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    entropy_key = Column(Float)
    data_hash = Column(Integer)
    correlation = Column(Float)
    measurements = Column(JSON)
    is_attack = Column(Boolean, default=False)

class SystemState(Base):
    __tablename__ = 'system_state'
    
    id = Column(Integer, primary_key=True, index=True)
    system_version = Column(Integer, default=1)
    total_resets = Column(Integer, default=0)
    quantum_intact = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def get_or_create_system_state(db):
    state = db.query(SystemState).first()
    if not state:
        state = SystemState()
        db.add(state)
        db.commit()
        db.refresh(state)
    return state

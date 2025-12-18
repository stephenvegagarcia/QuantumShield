import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    # Use SQLite as fallback for testing
    DATABASE_URL = 'sqlite:///quantum_security.db'
    logger.warning("DATABASE_URL not set. Using SQLite fallback: quantum_security.db")

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

class ProcessEvent(Base):
    __tablename__ = 'process_events'
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    process_name = Column(String(255))
    process_id = Column(Integer)
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    threat_score = Column(Float, default=0.0)
    is_suspicious = Column(Boolean, default=False)
    details = Column(JSON)

class ThreatSignature(Base):
    __tablename__ = 'threat_signatures'
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    threat_type = Column(String(50))
    signature_pattern = Column(Text)
    severity = Column(String(20))
    file_extensions = Column(JSON)
    process_names = Column(JSON)
    behavior_patterns = Column(JSON)
    detection_count = Column(Integer, default=0)
    last_detected = Column(DateTime, nullable=True)

class AutomatedResponse(Base):
    __tablename__ = 'automated_responses'
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    threat_id = Column(Integer, nullable=True)
    response_type = Column(String(50))
    action_taken = Column(Text)
    target = Column(String(500))
    success = Column(Boolean, default=True)
    details = Column(JSON)

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

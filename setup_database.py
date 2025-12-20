#!/usr/bin/env python3
"""
Database Setup and Management Script
Initialize, reset, or check database status
"""

import sys
import os
from datetime import datetime

# Set default DATABASE_URL if not set
if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///./quantumshield.db'

from database import (
    init_db, get_db, SecurityEvent, MonitoredFile, 
    QuantumMeasurement, SystemState, ProcessEvent,
    ThreatSignature, AutomatedResponse
)

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print('='*60)

def initialize_database():
    """Initialize database with all tables"""
    print_header("Initializing Database")
    print(f"Database URL: {os.getenv('DATABASE_URL')}")
    
    try:
        init_db()
        print("✅ Database initialized successfully!")
        
        # Verify tables
        db = get_db()
        try:
            tables = {
                'security_events': SecurityEvent,
                'monitored_files': MonitoredFile,
                'quantum_measurements': QuantumMeasurement,
                'system_state': SystemState,
                'process_events': ProcessEvent,
                'threat_signatures': ThreatSignature,
                'automated_responses': AutomatedResponse
            }
            
            print("\nTables created:")
            for table_name, model in tables.items():
                count = db.query(model).count()
                print(f"  ✓ {table_name} ({count} records)")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def check_status():
    """Check database status and statistics"""
    print_header("Database Status")
    print(f"Database URL: {os.getenv('DATABASE_URL')}")
    
    db = get_db()
    try:
        stats = {
            'Security Events': db.query(SecurityEvent).count(),
            'Monitored Files': db.query(MonitoredFile).count(),
            'Quantum Measurements': db.query(QuantumMeasurement).count(),
            'System States': db.query(SystemState).count(),
            'Process Events': db.query(ProcessEvent).count(),
            'Threat Signatures': db.query(ThreatSignature).count(),
            'Automated Responses': db.query(AutomatedResponse).count(),
        }
        
        print("\nRecord Counts:")
        for table, count in stats.items():
            print(f"  {table:.<30} {count:>5}")
        
        # Check latest events
        latest_event = db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).first()
        if latest_event:
            print(f"\nLatest Security Event:")
            print(f"  Time: {latest_event.timestamp}")
            print(f"  Type: {latest_event.event_type}")
            print(f"  Reason: {latest_event.reason}")
        
        # Check system state
        state = db.query(SystemState).first()
        if state:
            print(f"\nSystem State:")
            print(f"  Version: {state.system_version}")
            print(f"  Total Resets: {state.total_resets}")
            print(f"  Quantum Intact: {state.quantum_intact}")
            print(f"  Last Updated: {state.last_updated}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        db.close()

def add_sample_data():
    """Add sample data for testing"""
    print_header("Adding Sample Data")
    
    db = get_db()
    try:
        # Add sample security event
        event = SecurityEvent(
            event_type="system_check",
            reason="Sample security event for testing",
            entropy=0.75,
            correlation=0.88
        )
        db.add(event)
        
        # Add sample quantum measurement
        measurement = QuantumMeasurement(
            entropy_key=0.7854,
            data_hash=123456,
            correlation=0.90,
            measurements={"00": 0.5, "11": 0.5},
            is_attack=False
        )
        db.add(measurement)
        
        # Add sample process event
        process = ProcessEvent(
            process_name="python",
            process_id=1234,
            cpu_percent=5.5,
            memory_percent=2.3,
            threat_score=0.1,
            is_suspicious=False,
            details={"status": "normal"}
        )
        db.add(process)
        
        db.commit()
        print("✅ Sample data added successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        db.close()

def reset_database():
    """Reset database (WARNING: deletes all data)"""
    print_header("Reset Database")
    print("⚠️  WARNING: This will delete ALL data!")
    
    response = input("Are you sure? Type 'yes' to continue: ")
    if response.lower() != 'yes':
        print("Cancelled.")
        return
    
    db_url = os.getenv('DATABASE_URL')
    
    # For SQLite, just delete the file
    if db_url.startswith('sqlite:///'):
        db_file = db_url.replace('sqlite:///', '')
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"✅ Deleted database file: {db_file}")
    
    # Re-initialize
    initialize_database()
    print("✅ Database reset complete!")

def show_help():
    """Show help message"""
    print("""
QuantumShield Database Management

Usage: python setup_database.py [command]

Commands:
  init        Initialize database (create tables)
  status      Check database status and statistics
  sample      Add sample data for testing
  reset       Reset database (WARNING: deletes all data)
  help        Show this help message

Environment Variables:
  DATABASE_URL    Database connection string
                  Default: sqlite:///./quantumshield.db
                  Example: postgresql://user:pass@localhost/db

Examples:
  python setup_database.py init
  python setup_database.py status
  
  DATABASE_URL=postgresql://user:pass@localhost/db python setup_database.py init
    """)

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    commands = {
        'init': initialize_database,
        'status': check_status,
        'sample': add_sample_data,
        'reset': reset_database,
        'help': show_help,
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

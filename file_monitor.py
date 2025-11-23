import os
import hashlib
import numpy as np
from datetime import datetime
from database import MonitoredFile, SecurityEvent, get_db

def calculate_file_entropy(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        if len(data) == 0:
            return 0.0
        
        byte_counts = np.bincount(np.frombuffer(data, dtype=np.uint8), minlength=256)
        probabilities = byte_counts[byte_counts > 0] / len(data)
        entropy = -np.sum(probabilities * np.log2(probabilities))
        
        return float(entropy)
    except Exception as e:
        return 0.0

def calculate_file_hash(file_path):
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return ""

def add_monitored_file(file_path):
    db = get_db()
    try:
        existing = db.query(MonitoredFile).filter_by(file_path=file_path).first()
        if existing:
            return existing, False
        
        entropy = calculate_file_entropy(file_path)
        file_hash = calculate_file_hash(file_path)
        
        monitored = MonitoredFile(
            file_path=file_path,
            entropy_signature=entropy,
            last_hash=file_hash
        )
        db.add(monitored)
        db.commit()
        db.refresh(monitored)
        
        return monitored, True
    finally:
        db.close()

def check_file_integrity(monitored_file):
    current_hash = calculate_file_hash(monitored_file.file_path)
    current_entropy = calculate_file_entropy(monitored_file.file_path)
    
    hash_changed = current_hash != monitored_file.last_hash
    entropy_drift = abs(current_entropy - monitored_file.entropy_signature)
    
    return {
        'hash_changed': hash_changed,
        'entropy_drift': entropy_drift,
        'current_hash': current_hash,
        'current_entropy': current_entropy,
        'compromised': hash_changed or entropy_drift > 0.5
    }

def scan_all_monitored_files():
    db = get_db()
    try:
        files = db.query(MonitoredFile).filter_by(is_active=True).all()
        results = []
        
        for mf in files:
            if not os.path.exists(mf.file_path):
                continue
            
            integrity = check_file_integrity(mf)
            
            if integrity['compromised']:
                mf.attack_count += 1
                mf.last_hash = integrity['current_hash']
                mf.entropy_signature = integrity['current_entropy']
                
                event = SecurityEvent(
                    event_type='File Tampering Detected',
                    reason=f'File {os.path.basename(mf.file_path)} modified - Hash/Entropy changed',
                    entropy=integrity['current_entropy']
                )
                db.add(event)
            
            mf.last_checked = datetime.utcnow()
            results.append({
                'file_path': mf.file_path,
                'file_id': mf.id,
                'integrity': integrity
            })
        
        db.commit()
        return results
    finally:
        db.close()

def get_all_monitored_files():
    db = get_db()
    try:
        files = db.query(MonitoredFile).filter_by(is_active=True).order_by(MonitoredFile.created_at.desc()).all()
        file_list = []
        for f in files:
            file_list.append({
                'id': f.id,
                'file_path': f.file_path,
                'created_at': f.created_at,
                'entropy_signature': f.entropy_signature,
                'last_hash': f.last_hash
            })
        return file_list
    finally:
        db.close()

def remove_monitored_file(file_id):
    db = get_db()
    try:
        mf = db.query(MonitoredFile).filter_by(id=file_id).first()
        if mf:
            mf.is_active = False
            db.commit()
            return True
        return False
    finally:
        db.close()

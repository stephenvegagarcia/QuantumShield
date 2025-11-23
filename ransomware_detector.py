import os
import time
from datetime import datetime, timedelta
from collections import defaultdict
from database import SecurityEvent, AutomatedResponse, MonitoredFile, get_db
import shutil

RANSOMWARE_EXTENSIONS = [
    '.encrypted', '.locked', '.crypto', '.crypt', '.locky', '.cerber',
    '.zepto', '.odin', '.thor', '.aesir', '.zzzzz', '.micro', '.cryptowall',
    '.vault', '.xtbl', '.crinf', '.r5a', '.XRNT', '.XTBL', '.crypt', '.R16M01D05',
    '.pzdc', '.good', '.LOL!', '.OMG!', '.RDM', '.RRK', '.encryptedRSA',
    '.crjoker', '.LeChiffre', '.keybtc@inbox_com', '.0x0', '.bleep', '.1999',
    '.oxar', '.darkness', '.wcry', '.wncry', '.wnry', '.onion'
]

RAPID_ENCRYPTION_THRESHOLD = 10
TIME_WINDOW_SECONDS = 60

class RansomwareDetector:
    def __init__(self):
        self.file_modification_tracker = defaultdict(list)
        self.file_mtime_cache = {}
        self.backup_directory = '/tmp/quantum_security_backups'
        os.makedirs(self.backup_directory, exist_ok=True)
    
    def check_file_extension(self, filepath):
        _, ext = os.path.splitext(filepath)
        return ext.lower() in RANSOMWARE_EXTENSIONS
    
    def track_file_modification(self, filepath):
        if not os.path.exists(filepath):
            return 0
        
        try:
            current_mtime = os.path.getmtime(filepath)
            current_time = time.time()
            parent_dir = os.path.dirname(filepath)
            
            if filepath in self.file_mtime_cache:
                if current_mtime > self.file_mtime_cache[filepath]:
                    self.file_modification_tracker[parent_dir].append(current_time)
            else:
                pass
            
            self.file_mtime_cache[filepath] = current_mtime
            
            recent_modifications = [
                t for t in self.file_modification_tracker[parent_dir]
                if current_time - t <= TIME_WINDOW_SECONDS
            ]
            self.file_modification_tracker[parent_dir] = recent_modifications
            
            return len(recent_modifications)
        except Exception:
            return 0
    
    def detect_rapid_encryption(self, directory):
        if directory not in self.file_modification_tracker:
            return False
        
        current_time = time.time()
        recent_modifications = [
            t for t in self.file_modification_tracker[directory]
            if current_time - t <= TIME_WINDOW_SECONDS
        ]
        
        return len(recent_modifications) >= RAPID_ENCRYPTION_THRESHOLD
    
    def create_backup(self, filepath):
        if not os.path.exists(filepath):
            return None
        
        try:
            filename = os.path.basename(filepath)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{timestamp}_{filename}"
            backup_path = os.path.join(self.backup_directory, backup_filename)
            
            shutil.copy2(filepath, backup_path)
            
            db = get_db()
            try:
                response = AutomatedResponse(
                    response_type='File Backup',
                    action_taken=f'Created backup of {filename} before potential encryption',
                    target=filepath,
                    success=True,
                    details={'backup_path': backup_path, 'original': filepath}
                )
                db.add(response)
                db.commit()
            finally:
                db.close()
            
            return backup_path
        except Exception as e:
            return None
    
    def scan_directory_for_ransomware(self, directory):
        threats_found = []
        
        if not os.path.exists(directory):
            return threats_found
        
        try:
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    
                    if self.check_file_extension(filepath):
                        threats_found.append({
                            'type': 'Ransomware Extension',
                            'file': filepath,
                            'severity': 'CRITICAL',
                            'details': f'Suspicious ransomware extension detected: {os.path.splitext(filepath)[1]}'
                        })
                    
                    num_mods = self.track_file_modification(filepath)
                    if num_mods >= RAPID_ENCRYPTION_THRESHOLD:
                        self.create_backup(filepath)
                        threats_found.append({
                            'type': 'Rapid Encryption',
                            'file': filepath,
                            'severity': 'CRITICAL',
                            'details': f'Detected {num_mods} modifications in {TIME_WINDOW_SECONDS} seconds'
                        })
        
        except Exception as e:
            pass
        
        if threats_found:
            self.log_ransomware_detection(threats_found)
        
        return threats_found
    
    def log_ransomware_detection(self, threats):
        db = get_db()
        try:
            for threat in threats:
                event = SecurityEvent(
                    event_type='Ransomware Detected',
                    reason=f"{threat['type']}: {threat['details']}",
                    system_version=1
                )
                db.add(event)
            
            db.commit()
        finally:
            db.close()
    
    def monitor_monitored_files(self):
        db = get_db()
        try:
            monitored_files = db.query(MonitoredFile).filter_by(is_active=True).all()
            threats = []
            
            for mf in monitored_files:
                if self.check_file_extension(mf.file_path):
                    threats.append({
                        'type': 'Ransomware Extension on Monitored File',
                        'file': mf.file_path,
                        'severity': 'CRITICAL',
                        'details': f'Monitored file has been encrypted: {mf.file_path}'
                    })
                    
                    backup_path = self.create_backup(mf.file_path)
                    
                    if backup_path:
                        response = AutomatedResponse(
                            response_type='Emergency Backup',
                            action_taken=f'Emergency backup created for monitored file',
                            target=mf.file_path,
                            success=True,
                            details={'backup': backup_path}
                        )
                        db.add(response)
            
            if threats:
                self.log_ransomware_detection(threats)
                db.commit()
            
            return threats
        finally:
            db.close()
    
    def get_recent_threats(self, limit=20):
        db = get_db()
        try:
            return db.query(SecurityEvent).filter(
                SecurityEvent.event_type.like('%Ransomware%')
            ).order_by(SecurityEvent.timestamp.desc()).limit(limit).all()
        finally:
            db.close()

ransomware_detector = RansomwareDetector()

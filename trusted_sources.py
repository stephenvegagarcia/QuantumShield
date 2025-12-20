"""
QuantumShield - Trusted Security Sources Verification Module
Validates files, processes, and network connections against trusted security sources
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Set
import requests

class TrustedSourcesManager:
    """Manages verification against trusted security sources"""
    
    def __init__(self):
        self.trusted_hashes_file = "trusted_hashes.json"
        self.trusted_domains_file = "trusted_domains.json"
        self.trusted_certificates_file = "trusted_certificates.json"
        self.load_trusted_sources()
        
    def load_trusted_sources(self):
        """Load all trusted sources from storage"""
        # Trusted file hashes
        if os.path.exists(self.trusted_hashes_file):
            with open(self.trusted_hashes_file, 'r') as f:
                self.trusted_hashes = json.load(f)
        else:
            self.trusted_hashes = {
                "system_files": [],
                "applications": [],
                "user_approved": []
            }
            
        # Trusted domains
        if os.path.exists(self.trusted_domains_file):
            with open(self.trusted_domains_file, 'r') as f:
                self.trusted_domains = json.load(f)
        else:
            self.trusted_domains = {
                "verified_sources": [
                    "github.com",
                    "microsoft.com",
                    "google.com",
                    "python.org",
                    "pypi.org"
                ],
                "security_vendors": [
                    "virustotal.com",
                    "malwarebytes.com",
                    "kaspersky.com"
                ],
                "user_approved": []
            }
            
        # Trusted certificates
        if os.path.exists(self.trusted_certificates_file):
            with open(self.trusted_certificates_file, 'r') as f:
                self.trusted_certificates = json.load(f)
        else:
            self.trusted_certificates = {
                "ca_fingerprints": [],
                "verified_signatures": []
            }
    
    def save_trusted_sources(self):
        """Save all trusted sources to storage"""
        with open(self.trusted_hashes_file, 'w') as f:
            json.dump(self.trusted_hashes, f, indent=2)
        with open(self.trusted_domains_file, 'w') as f:
            json.dump(self.trusted_domains, f, indent=2)
        with open(self.trusted_certificates_file, 'w') as f:
            json.dump(self.trusted_certificates, f, indent=2)
    
    def calculate_file_hash(self, filepath: str) -> Optional[str]:
        """Calculate SHA-256 hash of a file"""
        try:
            sha256_hash = hashlib.sha256()
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return None
    
    def verify_file_hash(self, filepath: str) -> Dict:
        """Verify if a file's hash is in trusted sources"""
        file_hash = self.calculate_file_hash(filepath)
        if not file_hash:
            return {
                "trusted": False,
                "reason": "Unable to calculate file hash",
                "hash": None
            }
        
        # Check all trusted hash categories
        for category, hashes in self.trusted_hashes.items():
            if file_hash in hashes:
                return {
                    "trusted": True,
                    "reason": f"Found in {category}",
                    "hash": file_hash,
                    "category": category
                }
        
        return {
            "trusted": False,
            "reason": "Hash not in trusted sources",
            "hash": file_hash
        }
    
    def add_trusted_hash(self, filepath: str, category: str = "user_approved") -> bool:
        """Add a file hash to trusted sources"""
        file_hash = self.calculate_file_hash(filepath)
        if not file_hash:
            return False
        
        if category not in self.trusted_hashes:
            self.trusted_hashes[category] = []
        
        if file_hash not in self.trusted_hashes[category]:
            self.trusted_hashes[category].append(file_hash)
            self.save_trusted_sources()
            return True
        return False
    
    def verify_domain(self, domain: str) -> Dict:
        """Verify if a domain is trusted"""
        domain = domain.lower().strip()
        
        # Check all trusted domain categories
        for category, domains in self.trusted_domains.items():
            if domain in domains or any(domain.endswith(d) for d in domains):
                return {
                    "trusted": True,
                    "reason": f"Found in {category}",
                    "domain": domain,
                    "category": category
                }
        
        return {
            "trusted": False,
            "reason": "Domain not in trusted sources",
            "domain": domain
        }
    
    def add_trusted_domain(self, domain: str, category: str = "user_approved") -> bool:
        """Add a domain to trusted sources"""
        domain = domain.lower().strip()
        
        if category not in self.trusted_domains:
            self.trusted_domains[category] = []
        
        if domain not in self.trusted_domains[category]:
            self.trusted_domains[category].append(domain)
            self.save_trusted_sources()
            return True
        return False
    
    def check_virustotal(self, file_hash: str, api_key: Optional[str] = None) -> Dict:
        """Check file hash against VirusTotal (requires API key)"""
        if not api_key:
            api_key = os.environ.get('VIRUSTOTAL_API_KEY')
        
        if not api_key:
            return {
                "checked": False,
                "reason": "VirusTotal API key not configured"
            }
        
        try:
            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            headers = {"x-apikey": api_key}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                malicious = stats.get('malicious', 0)
                suspicious = stats.get('suspicious', 0)
                
                return {
                    "checked": True,
                    "trusted": malicious == 0 and suspicious == 0,
                    "malicious_count": malicious,
                    "suspicious_count": suspicious,
                    "total_engines": sum(stats.values())
                }
            else:
                return {
                    "checked": False,
                    "reason": f"VirusTotal returned status {response.status_code}"
                }
        except Exception as e:
            return {
                "checked": False,
                "reason": f"Error checking VirusTotal: {str(e)}"
            }
    
    def get_trust_score(self, filepath: str) -> Dict:
        """Calculate overall trust score for a file"""
        results = {
            "filepath": filepath,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "trust_score": 0,
            "recommendation": "UNKNOWN"
        }
        
        # Check hash
        hash_result = self.verify_file_hash(filepath)
        results["checks"]["hash_verification"] = hash_result
        if hash_result["trusted"]:
            results["trust_score"] += 50
        
        # Check file size (suspiciously small or large files)
        try:
            file_size = os.path.getsize(filepath)
            results["checks"]["file_size"] = {
                "size": file_size,
                "suspicious": file_size < 100 or file_size > 100_000_000
            }
            if not results["checks"]["file_size"]["suspicious"]:
                results["trust_score"] += 20
        except:
            results["checks"]["file_size"] = {"error": "Unable to get file size"}
        
        # Check file extension
        ext = os.path.splitext(filepath)[1].lower()
        dangerous_extensions = ['.exe', '.dll', '.bat', '.cmd', '.ps1', '.vbs', '.js']
        results["checks"]["file_extension"] = {
            "extension": ext,
            "potentially_dangerous": ext in dangerous_extensions
        }
        if ext not in dangerous_extensions:
            results["trust_score"] += 30
        
        # Determine recommendation
        if results["trust_score"] >= 80:
            results["recommendation"] = "TRUSTED"
        elif results["trust_score"] >= 50:
            results["recommendation"] = "CAUTION"
        else:
            results["recommendation"] = "SUSPICIOUS"
        
        return results
    
    def get_all_trusted_sources(self) -> Dict:
        """Get summary of all trusted sources"""
        return {
            "trusted_hashes": {
                category: len(hashes) 
                for category, hashes in self.trusted_hashes.items()
            },
            "trusted_domains": {
                category: len(domains) 
                for category, domains in self.trusted_domains.items()
            },
            "trusted_certificates": {
                category: len(certs) 
                for category, certs in self.trusted_certificates.items()
            }
        }

# Global instance
trusted_sources_manager = TrustedSourcesManager()

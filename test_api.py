#!/usr/bin/env python3
"""
QuantumShield API Test Script
Test all API endpoints and verify functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_health():
    """Test health check endpoint"""
    print_section("Health Check")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_stats():
    """Test system statistics"""
    print_section("System Statistics")
    response = requests.get(f"{BASE_URL}/api/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_create_event():
    """Test creating a security event"""
    print_section("Create Security Event")
    event_data = {
        "event_type": "test_event",
        "reason": "Testing API endpoint",
        "entropy": 0.85,
        "correlation": 0.92,
        "system_version": 1
    }
    response = requests.post(f"{BASE_URL}/api/events", json=event_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json().get('id')

def test_get_events():
    """Test getting recent events"""
    print_section("Get Recent Events")
    response = requests.get(f"{BASE_URL}/api/events/recent?limit=5")
    print(f"Status: {response.status_code}")
    events = response.json()
    print(f"Found {len(events)} events:")
    for event in events:
        print(f"  - [{event['timestamp']}] {event['event_type']}: {event['reason']}")

def test_create_quantum_measurement():
    """Test creating a quantum measurement"""
    print_section("Create Quantum Measurement")
    measurement_data = {
        "entropy_key": 0.7854,
        "data_hash": 12345678,
        "correlation": 0.88,
        "measurements": {"00": 0.5, "11": 0.5},
        "is_attack": False
    }
    response = requests.post(f"{BASE_URL}/api/quantum/measurements", json=measurement_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_quantum_measurements():
    """Test getting quantum measurements"""
    print_section("Get Quantum Measurements")
    response = requests.get(f"{BASE_URL}/api/quantum/measurements?limit=5")
    print(f"Status: {response.status_code}")
    measurements = response.json()
    print(f"Found {len(measurements)} measurements:")
    for m in measurements:
        print(f"  - [{m['timestamp']}] Entropy: {m['entropy_key']:.4f}, Attack: {m['is_attack']}")

def test_system_state():
    """Test system state endpoints"""
    print_section("Get System State")
    response = requests.get(f"{BASE_URL}/api/system/state")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\nUpdating system state...")
    update_data = {
        "total_resets": 5,
        "quantum_intact": True
    }
    response = requests.put(f"{BASE_URL}/api/system/state", json=update_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_monitored_files():
    """Test monitored files endpoint"""
    print_section("Get Monitored Files")
    response = requests.get(f"{BASE_URL}/api/files/monitored")
    print(f"Status: {response.status_code}")
    files = response.json()
    print(f"Found {len(files)} monitored files:")
    for f in files[:5]:  # Show first 5
        print(f"  - {f['file_path']} (Active: {f['is_active']}, Attacks: {f['attack_count']})")

def test_processes():
    """Test process endpoints"""
    print_section("Get Recent Processes")
    response = requests.get(f"{BASE_URL}/api/processes/recent?limit=5")
    print(f"Status: {response.status_code}")
    processes = response.json()
    print(f"Found {len(processes)} recent processes:")
    for p in processes:
        print(f"  - {p['process_name']} (PID: {p['process_id']}, Threat: {p['threat_score']:.2f})")
    
    print("\nGetting suspicious processes...")
    response = requests.get(f"{BASE_URL}/api/processes/suspicious")
    print(f"Status: {response.status_code}")
    suspicious = response.json()
    print(f"Found {len(suspicious)} suspicious processes")

def test_threats():
    """Test threat signatures endpoint"""
    print_section("Get Threat Signatures")
    response = requests.get(f"{BASE_URL}/api/threats/signatures")
    print(f"Status: {response.status_code}")
    threats = response.json()
    print(f"Found {len(threats)} threat signatures:")
    for t in threats[:5]:  # Show first 5
        print(f"  - {t['threat_type']} (Severity: {t['severity']}, Detections: {t['detection_count']})")

def test_automated_responses():
    """Test automated responses endpoint"""
    print_section("Get Automated Responses")
    response = requests.get(f"{BASE_URL}/api/responses/automated?limit=5")
    print(f"Status: {response.status_code}")
    responses = response.json()
    print(f"Found {len(responses)} automated responses:")
    for r in responses:
        print(f"  - [{r['timestamp']}] {r['response_type']}: {r['action_taken']}")

def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("  QuantumShield API Test Suite")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        test_health()
        test_stats()
        test_create_event()
        test_get_events()
        test_create_quantum_measurement()
        test_get_quantum_measurements()
        test_system_state()
        test_monitored_files()
        test_processes()
        test_threats()
        test_automated_responses()
        
        print_section("All Tests Completed Successfully! ✓")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Flask server.")
        print("Make sure the Flask app is running:")
        print("  export DATABASE_URL=sqlite:///./quantumshield.db")
        print("  python flask_app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    run_all_tests()

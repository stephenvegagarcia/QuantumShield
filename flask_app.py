from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.visualization import circuit_drawer
from qiskit.quantum_info import Statevector
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Flask
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import time
import os
import secrets

from database import init_db, get_db, SecurityEvent, QuantumMeasurement, SystemState, get_or_create_system_state, ProcessEvent, AutomatedResponse
from file_monitor import add_monitored_file, scan_all_monitored_files, get_all_monitored_files, remove_monitored_file
from malware_detector import scan_running_processes, terminate_suspicious_process, get_suspicious_processes_history, get_recent_automated_responses
from ransomware_detector import ransomware_detector, RANSOMWARE_EXTENSIONS

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Initialize database
init_db()

def init_session():
    """Initialize session variables"""
    if 'initialized' not in session:
        db = get_db()
        try:
            sys_state = get_or_create_system_state(db)
            session['system_version'] = sys_state.system_version
            session['system_resets'] = sys_state.total_resets
            session['quantum_intact'] = sys_state.quantum_intact
            
            security_events = db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).limit(50).all()
            session['attack_count'] = len(security_events)
            
            all_measurements = db.query(QuantumMeasurement).all()
            measurements_dict = {'00': 0, '11': 0, 'other': 0}
            for qm in all_measurements:
                if qm.measurements:
                    for state, count in qm.measurements.items():
                        if state in ['00', '11']:
                            measurements_dict[state] += count
                        else:
                            measurements_dict['other'] += count
            session['measurements'] = measurements_dict
            
            session['initialized'] = True
        finally:
            db.close()

def create_bell_state():
    """Create a Bell state quantum circuit"""
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)
    
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    
    return qc

def calculate_entropy(counts):
    """Calculate Shannon entropy"""
    total = sum(counts.values())
    entropy = 0
    for count in counts.values():
        if count > 0:
            prob = count / total
            entropy -= prob * np.log2(prob)
    return entropy

def get_statevector(qc):
    """Get quantum state vector"""
    backend = Aer.get_backend('statevector_simulator')
    result = backend.run(qc).result()
    statevector = result.get_statevector()
    return statevector

def measure_quantum_state(qc):
    """Measure quantum state"""
    qr = qc.qregs[0]
    cr = qc.cregs[0]
    
    qc_measure = qc.copy()
    qc_measure.measure(qr, cr)
    
    backend = Aer.get_backend('qasm_simulator')
    job = backend.run(qc_measure, shots=1000)
    result = job.result()
    counts = result.get_counts()
    
    return counts

def simulate_attack(qc):
    """Simulate an attack on the quantum state"""
    qr = qc.qregs[0]
    cr = qc.cregs[0]
    
    qc_attacked = qc.copy()
    
    qc_attacked.measure(qr[0], cr[0])
    qc_attacked.barrier()
    qc_attacked.h(qr[1])
    qc_attacked.z(qr[0])
    qc_attacked.measure(qr, cr)
    
    backend = Aer.get_backend('qasm_simulator')
    job = backend.run(qc_attacked, shots=1000)
    result = job.result()
    counts = result.get_counts()
    
    return counts

def store_quantum_data_with_entropy(counts, timestamp, is_attack=False):
    """Store quantum measurement data with entropy"""
    entropy = calculate_entropy(counts)
    
    data_hash = int(entropy * 1000) % 256
    correlation = (counts.get('00', 0) + counts.get('11', 0)) / sum(counts.values()) * 100
    
    entropy_float = float(entropy)
    correlation_float = float(correlation)
    
    db = get_db()
    try:
        qm = QuantumMeasurement(
            entropy_key=entropy_float,
            data_hash=data_hash,
            correlation=correlation_float,
            measurements=counts,
            is_attack=is_attack
        )
        db.add(qm)
        db.commit()
    finally:
        db.close()
    
    return entropy_float

def detect_attack(counts):
    """Detect if an attack has occurred"""
    total = sum(counts.values())
    if total == 0:
        return True  # Consider empty counts as an attack
    bell_correlation = counts.get('00', 0) + counts.get('11', 0)
    correlation_ratio = bell_correlation / total
    
    return correlation_ratio < 0.95

def upgrade_system():
    """Upgrade the system version"""
    session['system_version'] = session.get('system_version', 1) + 1
    
    db = get_db()
    try:
        sys_state = get_or_create_system_state(db)
        sys_state.system_version = session['system_version']
        sys_state.last_updated = datetime.utcnow()
        
        event = SecurityEvent(
            event_type='System Upgrade',
            reason=f'Upgraded to version {session["system_version"]} - Quantum coherence maintained',
            system_version=session['system_version']
        )
        db.add(event)
        db.commit()
    finally:
        db.close()

def auto_reset_system():
    """Auto reset the system after attack"""
    session['system_resets'] = session.get('system_resets', 0) + 1
    session['quantum_intact'] = True
    
    db = get_db()
    try:
        sys_state = get_or_create_system_state(db)
        sys_state.total_resets = session['system_resets']
        sys_state.quantum_intact = True
        sys_state.last_updated = datetime.utcnow()
        
        event = SecurityEvent(
            event_type='System Auto-Reset',
            reason='Quantum state restored to Bell state',
            system_version=session.get('system_version', 1)
        )
        db.add(event)
        db.commit()
    finally:
        db.close()

def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_base64

@app.route('/')
def index():
    """Main dashboard page"""
    init_session()
    
    # Create Bell state circuit
    qc = create_bell_state()
    
    # Generate circuit diagram
    fig = circuit_drawer(qc, output='mpl', style='iqp')
    circuit_img = fig_to_base64(fig)
    
    # Get attack log
    db = get_db()
    try:
        security_events = db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).limit(10).all()
        attack_log = [
            {
                'timestamp': event.timestamp.strftime("%H:%M:%S"),
                'event': event.event_type,
                'reason': event.reason
            }
            for event in reversed(security_events)
        ]
        
        # Get secure data store
        recent_measurements = db.query(QuantumMeasurement).order_by(QuantumMeasurement.timestamp.desc()).limit(5).all()
        secure_data_store = [
            {
                'timestamp': qm.timestamp.strftime("%H:%M:%S.%f")[:-3],
                'entropy_key': qm.entropy_key,
                'hash': qm.data_hash,
                'correlation': qm.correlation,
                'measurements': qm.measurements
            }
            for qm in reversed(recent_measurements)
        ]
        
        total_secure_entries = db.query(QuantumMeasurement).count()
        
    finally:
        db.close()
    
    return render_template('index.html',
                         circuit_img=circuit_img,
                         system_version=session.get('system_version', 1),
                         system_resets=session.get('system_resets', 0),
                         quantum_intact=session.get('quantum_intact', True),
                         attack_count=session.get('attack_count', 0),
                         measurements=session.get('measurements', {'00': 0, '11': 0, 'other': 0}),
                         attack_log=attack_log,
                         secure_data_store=secure_data_store,
                         total_secure_entries=total_secure_entries)

@app.route('/measure')
def measure():
    """Perform normal measurement"""
    init_session()
    
    qc = create_bell_state()
    measurements = measure_quantum_state(qc)
    
    # Store measurement
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    store_quantum_data_with_entropy(measurements, timestamp)
    
    # Update session measurements
    session_measurements = session.get('measurements', {'00': 0, '11': 0, 'other': 0})
    for state, count in measurements.items():
        if state in ['00', '11']:
            session_measurements[state] = session_measurements.get(state, 0) + count
        else:
            session_measurements['other'] = session_measurements.get('other', 0) + count
    session['measurements'] = session_measurements
    
    # Calculate correlation
    total = sum(measurements.values())
    bell_states = measurements.get('00', 0) + measurements.get('11', 0)
    correlation = (bell_states / total) * 100 if total > 0 else 0
    entropy = calculate_entropy(measurements)
    
    return jsonify({
        'success': True,
        'measurements': measurements,
        'correlation': f"{correlation:.1f}%",
        'entropy': f"{entropy:.4f}",
        'intact': correlation >= 95
    })

@app.route('/attack', methods=['POST'])
def attack():
    """Simulate an attack"""
    init_session()
    
    qc = create_bell_state()
    attack_counts = simulate_attack(qc)
    
    # Store attack measurement
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    attack_entropy = store_quantum_data_with_entropy(attack_counts, timestamp, is_attack=True)
    
    # Update session measurements
    session_measurements = session.get('measurements', {'00': 0, '11': 0, 'other': 0})
    for state, count in attack_counts.items():
        if state in ['00', '11']:
            session_measurements[state] = session_measurements.get(state, 0) + count
        else:
            session_measurements['other'] = session_measurements.get('other', 0) + count
    session['measurements'] = session_measurements
    
    # Log attack
    attack_reason = f'Eavesdropper introduced decoherence - Data secured with entropy {attack_entropy:.4f}'
    db = get_db()
    try:
        event = SecurityEvent(
            event_type='Attack Detected',
            reason=attack_reason,
            system_version=session.get('system_version', 1)
        )
        db.add(event)
        
        if detect_attack(attack_counts):
            session['quantum_intact'] = False
            sys_state = get_or_create_system_state(db)
            sys_state.quantum_intact = False
        
        db.commit()
    finally:
        db.close()
    
    # Calculate correlation
    total = sum(attack_counts.values())
    bell_states = attack_counts.get('00', 0) + attack_counts.get('11', 0)
    correlation = (bell_states / total) * 100 if total > 0 else 0
    
    return jsonify({
        'success': True,
        'measurements': attack_counts,
        'correlation': f"{correlation:.1f}%",
        'entropy': f"{attack_entropy:.4f}",
        'compromised': detect_attack(attack_counts)
    })

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the system"""
    init_session()
    auto_reset_system()
    return jsonify({'success': True, 'resets': session['system_resets']})

@app.route('/upgrade', methods=['POST'])
def upgrade():
    """Upgrade the system"""
    init_session()
    upgrade_system()
    return jsonify({'success': True, 'version': session['system_version']})

@app.route('/file-monitor')
def file_monitor():
    """File monitoring page"""
    init_session()
    
    monitored_files = get_all_monitored_files()
    
    return render_template('file_monitor.html',
                         monitored_files=monitored_files)

@app.route('/add-file', methods=['POST'])
def add_file():
    """Add a file to monitor"""
    file_path = request.form.get('file_path')
    
    if not file_path:
        return jsonify({'success': False, 'error': 'No file path provided'})
    
    # Security: Validate file path to prevent directory traversal
    file_path = os.path.abspath(file_path)
    
    # Security: Restrict to safe directories (optional - uncomment to enable)
    # allowed_dirs = ['/tmp', os.path.expanduser('~')]
    # if not any(file_path.startswith(d) for d in allowed_dirs):
    #     return jsonify({'success': False, 'error': 'File path not in allowed directories'})
    
    if not os.path.exists(file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write("")
        except Exception as e:
            return jsonify({'success': False, 'error': f'Could not create file: {str(e)}'})
    
    monitored, is_new = add_monitored_file(file_path)
    
    if is_new:
        db = get_db()
        try:
            event = SecurityEvent(
                event_type='File Added',
                reason=f'Started monitoring file: {file_path}',
                system_version=session.get('system_version', 1)
            )
            db.add(event)
            db.commit()
        finally:
            db.close()
    
    return jsonify({'success': True, 'is_new': is_new})

@app.route('/scan-files', methods=['POST'])
def scan_files():
    """Scan all monitored files"""
    results = scan_all_monitored_files()
    compromised = [r for r in results if r['integrity']['compromised']]
    
    return jsonify({
        'success': True,
        'total': len(results),
        'compromised': len(compromised),
        'results': compromised
    })

@app.route('/remove-file/<int:file_id>', methods=['POST'])
def remove_file(file_id):
    """Remove a file from monitoring"""
    success = remove_monitored_file(file_id)
    return jsonify({'success': success})

@app.route('/threat-detection')
def threat_detection():
    """Threat detection page"""
    init_session()
    
    # Get recent threat history
    suspicious_history = get_suspicious_processes_history(10)
    recent_responses = get_recent_automated_responses(10)
    
    return render_template('threat_detection.html',
                         suspicious_history=suspicious_history,
                         recent_responses=recent_responses,
                         monitored_files_count=len(get_all_monitored_files()))

@app.route('/scan-malware', methods=['POST'])
def scan_malware():
    """Scan for malware"""
    suspicious = scan_running_processes()
    
    return jsonify({
        'success': True,
        'count': len(suspicious),
        'processes': suspicious
    })

@app.route('/scan-ransomware', methods=['POST'])
def scan_ransomware():
    """Scan for ransomware"""
    ransom_threats = ransomware_detector.monitor_monitored_files()
    
    return jsonify({
        'success': True,
        'count': len(ransom_threats),
        'threats': ransom_threats
    })

@app.route('/terminate-process/<int:pid>', methods=['POST'])
def terminate_process(pid):
    """Terminate a suspicious process"""
    reason = request.form.get('reason', 'Manual termination')
    success = terminate_suspicious_process(pid, reason)
    
    return jsonify({'success': success})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

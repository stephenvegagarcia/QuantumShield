import streamlit as st
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.visualization import plot_bloch_multivector, plot_state_city
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime
import time
import os

from database import init_db, get_db, SecurityEvent, QuantumMeasurement, SystemState, get_or_create_system_state, ProcessEvent, AutomatedResponse
from file_monitor import add_monitored_file, scan_all_monitored_files, get_all_monitored_files, remove_monitored_file
from malware_detector import scan_running_processes, terminate_suspicious_process, get_suspicious_processes_history, get_recent_automated_responses
from ransomware_detector import ransomware_detector

init_db()

st.set_page_config(page_title="Quantum Security System", layout="wide")

st.title("🔐 Quantum Entanglement Self-Healing Security System")
st.markdown("### Bell State |φ⁺⟩ = 1/√2 (|00⟩ + |11⟩) - Now with Persistent File Protection")

if 'db_initialized' not in st.session_state:
    db = get_db()
    try:
        sys_state = get_or_create_system_state(db)
        st.session_state.system_version = sys_state.system_version
        st.session_state.system_resets = sys_state.total_resets
        st.session_state.quantum_intact = sys_state.quantum_intact
        
        security_events = db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).limit(50).all()
        st.session_state.attack_log = [
            {
                'timestamp': event.timestamp.strftime("%H:%M:%S"),
                'event': event.event_type,
                'reason': event.reason
            }
            for event in reversed(security_events)
        ]
        
        recent_measurements = db.query(QuantumMeasurement).order_by(QuantumMeasurement.timestamp.desc()).limit(100).all()
        st.session_state.entropy_storage = [qm.entropy_key for qm in reversed(recent_measurements)]
        st.session_state.secure_data_store = [
            {
                'timestamp': qm.timestamp.strftime("%H:%M:%S.%f")[:-3],
                'entropy_key': qm.entropy_key,
                'hash': qm.data_hash,
                'correlation': qm.correlation,
                'measurements': qm.measurements
            }
            for qm in reversed(recent_measurements)
        ]
        
        all_measurements = db.query(QuantumMeasurement).all()
        measurements_dict = {'00': 0, '11': 0, 'other': 0}
        for qm in all_measurements:
            if qm.measurements:
                for state, count in qm.measurements.items():
                    if state in ['00', '11']:
                        measurements_dict[state] += count
                    else:
                        measurements_dict['other'] += count
        st.session_state.measurements = measurements_dict
        
        st.session_state.db_initialized = True
    finally:
        db.close()

if 'last_attack_results' not in st.session_state:
    st.session_state.last_attack_results = None
if 'under_attack' not in st.session_state:
    st.session_state.under_attack = False

def create_bell_state():
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)
    
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    
    return qc

def calculate_entropy(counts):
    total = sum(counts.values())
    entropy = 0
    for count in counts.values():
        if count > 0:
            prob = count / total
            entropy -= prob * np.log2(prob)
    return entropy

def get_statevector(qc):
    backend = Aer.get_backend('statevector_simulator')
    result = backend.run(qc).result()
    statevector = result.get_statevector()
    return statevector

def measure_quantum_state(qc):
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
    entropy = calculate_entropy(counts)
    
    data_hash = int(entropy * 1000) % 256
    correlation = (counts.get('00', 0) + counts.get('11', 0)) / sum(counts.values()) * 100
    
    entropy_float = float(entropy)
    correlation_float = float(correlation)
    
    data_entry = {
        'timestamp': timestamp,
        'entropy_key': entropy_float,
        'hash': data_hash,
        'correlation': correlation_float,
        'measurements': counts
    }
    
    st.session_state.entropy_storage.append(entropy_float)
    st.session_state.secure_data_store.append(data_entry)
    
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

def upgrade_system():
    st.session_state.system_version += 1
    st.session_state.attack_log.append({
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'event': 'System Upgrade',
        'reason': f'Upgraded to version {st.session_state.system_version} - Quantum coherence maintained'
    })
    
    db = get_db()
    try:
        sys_state = get_or_create_system_state(db)
        sys_state.system_version = st.session_state.system_version
        sys_state.last_updated = datetime.utcnow()
        
        event = SecurityEvent(
            event_type='System Upgrade',
            reason=f'Upgraded to version {st.session_state.system_version} - Quantum coherence maintained',
            system_version=st.session_state.system_version
        )
        db.add(event)
        db.commit()
    finally:
        db.close()

def detect_attack(counts):
    total = sum(counts.values())
    bell_correlation = counts.get('00', 0) + counts.get('11', 0)
    correlation_ratio = bell_correlation / total
    
    return correlation_ratio < 0.95

def classical_processing(measurement_results, is_attack_data=False):
    st.subheader("📊 Classical Processing Layer")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Quantum Measurement Results**")
        for state, count in sorted(measurement_results.items()):
            st.metric(f"State |{state}⟩", count)
    
    with col2:
        total = sum(measurement_results.values())
        bell_states = measurement_results.get('00', 0) + measurement_results.get('11', 0)
        correlation = (bell_states / total) * 100 if total > 0 else 0
        
        st.markdown("**Entanglement Correlation**")
        st.metric("Bell State Correlation", f"{correlation:.1f}%")
        
        if is_attack_data:
            if correlation >= 95:
                st.success("✅ Attack Failed - Entanglement Intact")
            else:
                st.error("⚠️ State Collapse - Triggering Reset")
        else:
            if correlation >= 95:
                st.success("✅ Quantum Entanglement Intact")
            else:
                st.warning("⚠️ Anomaly Detected")
    
    with col3:
        entropy = calculate_entropy(measurement_results)
        st.markdown("**Quantum Entropy Security**")
        st.metric("Shannon Entropy", f"{entropy:.4f} bits")
        
        if not is_attack_data:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            store_quantum_data_with_entropy(measurement_results, timestamp)
            
            for state, count in measurement_results.items():
                st.session_state.measurements[state] = st.session_state.measurements.get(state, 0) + count
            
            st.success(f"✅ Data secured with entropy key")

def auto_reset_system():
    st.session_state.system_resets += 1
    st.session_state.attack_log.append({
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'event': 'System Auto-Reset',
        'reason': 'Quantum state restored to Bell state'
    })
    st.session_state.quantum_intact = True
    st.session_state.under_attack = False
    st.session_state.last_attack_results = None
    
    db = get_db()
    try:
        sys_state = get_or_create_system_state(db)
        sys_state.total_resets = st.session_state.system_resets
        sys_state.quantum_intact = True
        sys_state.last_updated = datetime.utcnow()
        
        event = SecurityEvent(
            event_type='System Auto-Reset',
            reason='Quantum state restored to Bell state',
            system_version=st.session_state.system_version
        )
        db.add(event)
        db.commit()
    finally:
        db.close()
    
    st.rerun()

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("⚛️ Quantum Circuit - Bell State Creation")
    
    qc = create_bell_state()
    
    fig = qc.draw(output='mpl', style='iqp')
    st.pyplot(fig)
    plt.close()
    
    st.markdown("""
    **Circuit Breakdown:**
    - **H Gate** (Hadamard): Creates superposition on qubit 0 → 1/√2 (|0⟩ + |1⟩)
    - **CNOT Gate**: Entangles qubits 0 and 1
    - **Result**: Bell state |φ⁺⟩ = 1/√2 (|00⟩ + |11⟩)
    - **Quantum Matrix**: Creates perfect correlation - measuring both gives 00 or 11
    """)

with col_right:
    st.subheader("🛡️ Security Status")
    
    if st.session_state.quantum_intact:
        st.success("🟢 **SYSTEM SECURE**")
        st.markdown("Quantum entanglement active")
    else:
        st.error("🔴 **ATTACK DETECTED**")
        st.markdown("Auto-resetting...")
    
    st.metric("System Resets", st.session_state.system_resets)
    st.metric("Attack Attempts", len(st.session_state.attack_log))

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Quantum State Vector")
    
    statevector = get_statevector(qc)
    
    fig_state = plot_state_city(statevector)
    st.pyplot(fig_state)
    plt.close()
    
    st.markdown("**Amplitudes:**")
    st.code(f"|00⟩: {statevector[0]:.4f}\n|01⟩: {statevector[1]:.4f}\n|10⟩: {statevector[2]:.4f}\n|11⟩: {statevector[3]:.4f}")

with col2:
    st.subheader("🎯 Bloch Sphere Representation")
    
    fig_bloch = plot_bloch_multivector(statevector)
    st.pyplot(fig_bloch)
    plt.close()

st.divider()

col_attack, col_measure = st.columns(2)

with col_attack:
    st.subheader("🎲 Simulate Attack")
    st.markdown("Attacking the system causes eavesdropping/measurement with decoherence")
    
    if st.button("🔴 Launch Attack", type="primary", use_container_width=True):
        attack_counts = simulate_attack(qc)
        
        for state, count in attack_counts.items():
            st.session_state.measurements[state] = st.session_state.measurements.get(state, 0) + count
        
        st.session_state.last_attack_results = attack_counts
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        attack_entropy = store_quantum_data_with_entropy(attack_counts, timestamp, is_attack=True)
        
        attack_reason = f'Eavesdropper introduced decoherence - Data secured with entropy {attack_entropy:.4f}'
        st.session_state.attack_log.append({
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'event': 'Attack Detected',
            'reason': attack_reason
        })
        
        db = get_db()
        try:
            sys_state = get_or_create_system_state(db)
            event = SecurityEvent(
                event_type='Attack Detected',
                reason=attack_reason,
                system_version=st.session_state.system_version
            )
            db.add(event)
            
            if detect_attack(attack_counts):
                st.session_state.quantum_intact = False
                st.session_state.under_attack = True
                sys_state.quantum_intact = False
            
            db.commit()
        finally:
            db.close()
        
        st.rerun()

with col_measure:
    st.subheader("🔄 System Controls")
    
    st.metric("System Version", f"v{st.session_state.system_version}")
    
    col_reset, col_upgrade = st.columns(2)
    
    with col_reset:
        if st.button("🔄 Reset", use_container_width=True):
            auto_reset_system()
    
    with col_upgrade:
        if st.button("⬆️ Upgrade", use_container_width=True):
            upgrade_system()
            st.rerun()

st.divider()

if st.session_state.last_attack_results is not None:
    st.info("⚠️ Displaying most recent attack measurement results - Data already secured")
    classical_processing(st.session_state.last_attack_results, is_attack_data=True)
else:
    measurements = measure_quantum_state(qc)
    classical_processing(measurements, is_attack_data=False)

if not st.session_state.quantum_intact:
    st.warning("⚠️ **Quantum state compromised! Auto-resetting in 2 seconds...**")
    time.sleep(2)
    auto_reset_system()

st.divider()

st.subheader("📜 Attack Log & System Events")

if st.session_state.attack_log:
    log_data = []
    for i, log in enumerate(reversed(st.session_state.attack_log[-10:])):
        log_data.append(f"{log['timestamp']} - {log['event']}: {log['reason']}")
    
    for entry in log_data:
        st.text(entry)
else:
    st.info("No attacks detected yet. System is secure.")

st.divider()

st.subheader("📊 Measurement Statistics")

col_stats1, col_stats2, col_stats3 = st.columns(3)

with col_stats1:
    st.metric("Total |00⟩ Measurements", st.session_state.measurements.get('00', 0))

with col_stats2:
    st.metric("Total |11⟩ Measurements", st.session_state.measurements.get('11', 0))

with col_stats3:
    other_count = sum(v for k, v in st.session_state.measurements.items() if k not in ['00', '11'])
    st.metric("Other States (Attack Indicator)", other_count)

total_measurements = sum(st.session_state.measurements.values())
if total_measurements > 0:
    fig = go.Figure(data=[go.Pie(
        labels=list(st.session_state.measurements.keys()),
        values=list(st.session_state.measurements.values()),
        hole=.3
    )])
    fig.update_layout(title="Measurement Distribution", height=400)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("🔐 Secure Quantum Data Store - Persists Through Collapse")
st.markdown("**Even when the quantum state collapses, the data remains secured with entropy keys**")

if st.session_state.secure_data_store:
    col_store1, col_store2 = st.columns([2, 1])
    
    with col_store1:
        st.markdown("**Latest Secured Data Entries**")
        for entry in reversed(st.session_state.secure_data_store[-5:]):
            with st.expander(f"📦 Entry {entry['timestamp']} - Hash: {entry['hash']:03d}"):
                st.write(f"**Entropy Key:** {entry['entropy_key']:.6f} bits")
                st.write(f"**Correlation:** {entry['correlation']:.2f}%")
                st.write(f"**Data Hash:** {entry['hash']:03d}")
                st.json(entry['measurements'])
    
    with col_store2:
        st.markdown("**Data Storage Stats**")
        st.metric("Total Secure Entries", len(st.session_state.secure_data_store))
        st.metric("Entropy Keys Generated", len(st.session_state.entropy_storage))
        
        if st.session_state.entropy_storage:
            avg_entropy = np.mean(st.session_state.entropy_storage)
            st.metric("Average Entropy", f"{avg_entropy:.4f} bits")
        
        entropy_trend = go.Figure()
        entropy_trend.add_trace(go.Scatter(
            y=st.session_state.entropy_storage,
            mode='lines+markers',
            name='Entropy',
            line=dict(color='cyan', width=2)
        ))
        entropy_trend.update_layout(
            title="Entropy Over Time",
            xaxis_title="Entry Number",
            yaxis_title="Shannon Entropy (bits)",
            height=300
        )
        st.plotly_chart(entropy_trend, use_container_width=True)
else:
    st.info("No data secured yet. Normal measurements will be automatically stored with entropy keys.")

st.divider()

st.subheader("🛡️ Active Threat Protection - Malware & Ransomware Defense")
st.markdown("**Real-time monitoring with quantum-enhanced detection and automated response**")

threat_tab1, threat_tab2, threat_tab3 = st.tabs(["🔴 Active Threats", "🦠 Process Monitor", "🔒 Ransomware Shield"])

with threat_tab1:
    st.markdown("### Live Threat Detection")
    
    col_scan1, col_scan2 = st.columns(2)
    
    with col_scan1:
        if st.button("🔍 Scan for Malware", use_container_width=True, type="primary"):
            with st.spinner("Scanning running processes..."):
                suspicious = scan_running_processes()
                
                if suspicious:
                    st.error(f"🚨 **{len(suspicious)} Suspicious Processes Detected!**")
                    for proc in suspicious:
                        with st.expander(f"⚠️ {proc['name']} (PID: {proc['pid']}) - Threat Score: {proc['threat_score']:.0f}"):
                            st.write(f"**CPU Usage:** {proc['cpu_percent']:.1f}%")
                            st.write(f"**Memory Usage:** {proc['memory_percent']:.1f}%")
                            st.write(f"**Threat Level:** {'CRITICAL' if proc['threat_score'] >= 70 else 'HIGH' if proc['threat_score'] >= 50 else 'MEDIUM'}")
                            
                            if st.button(f"🛑 Terminate Process", key=f"kill_{proc['pid']}"):
                                if terminate_suspicious_process(proc['pid'], f"High threat score: {proc['threat_score']}"):
                                    st.success(f"✅ Process {proc['pid']} terminated")
                                else:
                                    st.error(f"❌ Failed to terminate process {proc['pid']}")
                else:
                    st.success("✅ No suspicious processes detected - System clean!")
    
    with col_scan2:
        if st.button("🔎 Check for Ransomware", use_container_width=True, type="primary"):
            with st.spinner("Scanning for ransomware activity..."):
                ransom_threats = ransomware_detector.monitor_monitored_files()
                
                if ransom_threats:
                    st.error(f"🚨 **{len(ransom_threats)} Ransomware Threats Detected!**")
                    for threat in ransom_threats:
                        st.warning(f"**{threat['severity']}**: {threat['type']}")
                        st.text(f"File: {threat['file']}")
                        st.text(f"Details: {threat['details']}")
                else:
                    st.success("✅ No ransomware activity detected!")
    
    st.markdown("### Recent Threat History")
    suspicious_history = get_suspicious_processes_history(10)
    if suspicious_history:
        for proc in suspicious_history:
            threat_level = "🔴" if proc.threat_score >= 70 else "🟠" if proc.threat_score >= 50 else "🟡"
            st.text(f"{threat_level} {proc.timestamp.strftime('%H:%M:%S')} - {proc.process_name} (PID: {proc.process_id}) - Score: {proc.threat_score:.0f}")
    else:
        st.info("No threat history yet")

with threat_tab2:
    st.markdown("### System Process Monitoring")
    
    if st.button("📊 Refresh Process List", use_container_width=True):
        with st.spinner("Scanning system processes..."):
            scan_running_processes()
            st.success("Process scan complete!")
    
    st.markdown("**Suspicious Process Patterns Monitored:**")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown("""
        - High CPU usage (>80%)
        - High memory usage (>70%)
        - Suspicious process names
        - Excessive file access (>100 files)
        """)
    
    with col_p2:
        st.markdown("""
        - Excessive network connections (>50)
        - Known malware signatures
        - Unauthorized system modifications
        - Behavioral anomalies
        """)
    
    db = get_db()
    try:
        recent_processes = db.query(ProcessEvent).order_by(ProcessEvent.timestamp.desc()).limit(20).all()
        if recent_processes:
            st.markdown("### Recent Process Activity")
            for proc in recent_processes[:10]:
                status = "🔴 SUSPICIOUS" if proc.is_suspicious else "🟢 Normal"
                st.text(f"{status} - {proc.process_name} | CPU: {proc.cpu_percent:.1f}% | Mem: {proc.memory_percent:.1f}% | Score: {proc.threat_score:.0f}")
    finally:
        db.close()

with threat_tab3:
    st.markdown("### Ransomware Protection Status")
    
    col_r1, col_r2, col_r3 = st.columns(3)
    
    with col_r1:
        st.metric("Protected Files", len(get_all_monitored_files()))
    
    with col_r2:
        ransom_threats = ransomware_detector.get_recent_threats(100)
        st.metric("Ransomware Blocks", len(ransom_threats))
    
    with col_r3:
        responses = get_recent_automated_responses(100)
        backups = [r for r in responses if r.response_type in ['File Backup', 'Emergency Backup']]
        st.metric("Files Backed Up", len(backups))
    
    st.markdown("**Ransomware Extension Protection:**")
    from ransomware_detector import RANSOMWARE_EXTENSIONS
    st.info(f"Monitoring {len(RANSOMWARE_EXTENSIONS)} known ransomware file extensions")
    
    st.markdown("### Automated Response Log")
    recent_responses = get_recent_automated_responses(10)
    if recent_responses:
        for response in recent_responses:
            status_icon = "✅" if response.success else "❌"
            st.text(f"{status_icon} {response.timestamp.strftime('%H:%M:%S')} - {response.response_type}: {response.action_taken}")
    else:
        st.info("No automated responses yet")

st.divider()

st.subheader("📁 File Integrity Monitor - Real Security Protection")
st.markdown("**Monitor actual files and detect unauthorized changes using quantum-secured checksums**")

col_file1, col_file2 = st.columns([2, 1])

with col_file1:
    st.markdown("**Add File to Monitor**")
    new_file = st.text_input("File path to monitor:", placeholder="/path/to/important/file.txt")
    
    if st.button("➕ Add File", use_container_width=True):
        if new_file and os.path.exists(new_file):
            monitored, is_new = add_monitored_file(new_file)
            if is_new:
                st.success(f"✅ Now monitoring: {new_file}")
                db = get_db()
                try:
                    event = SecurityEvent(
                        event_type='File Added',
                        reason=f'Started monitoring file: {new_file}',
                        system_version=st.session_state.system_version
                    )
                    db.add(event)
                    db.commit()
                finally:
                    db.close()
                st.rerun()
            else:
                st.error("File already being monitored")
        elif new_file:
            st.error("File does not exist")

with col_file2:
    st.markdown("**Security Scan**")
    if st.button("🔍 Scan All Files", use_container_width=True, type="primary"):
        results = scan_all_monitored_files()
        compromised = [r for r in results if r['integrity']['compromised']]
        if compromised:
            for result in compromised:
                st.warning(f"⚠️ CHANGE DETECTED: {result['file_path']}")
                st.text(f"Entropy drift: {result['integrity']['entropy_drift']:.4f}")
                st.text(f"Hash changed: {result['integrity']['hash_changed']}")
            st.error(f"🚨 {len(compromised)} file(s) modified!")
        else:
            st.success("✅ All files intact - No changes detected")

st.markdown("**Monitored Files**")
monitored = get_all_monitored_files()
if monitored:
    for file in monitored:
        col_f1, col_f2, col_f3 = st.columns([3, 2, 1])
        with col_f1:
            st.text(f"📄 {file.file_path}")
        with col_f2:
            st.text(f"Added: {file.created_at.strftime('%Y-%m-%d %H:%M')}")
        with col_f3:
            if st.button("🗑️", key=f"remove_{file.id}"):
                remove_monitored_file(file.id)
                st.rerun()
else:
    st.info("No files being monitored yet. Add files above to start protecting them.")

st.divider()

st.markdown("""
### 🔬 How This Quantum Security System Works

1. **Quantum Matrix Creation**: Uses H(0) → CNOT(0,1) to create entangled Bell state |φ⁺⟩
2. **Perfect Correlation**: The Bell state |φ⁺⟩ = 1/√2 (|00⟩ + |11⟩) ensures measurements are always 00 or 11
3. **Entropy-Based Storage**: ALL measurements (normal + attack) are secured with Shannon entropy keys
4. **Data Persistence**: Even when quantum state collapses from attack, data is preserved in classical storage
5. **Attack Detection**: Eavesdropping introduces decoherence, breaking the perfect Bell correlation
6. **Auto-Reset**: System detects correlation drop and automatically restores to original quantum state
7. **System Upgrades**: Can upgrade versions over time while maintaining quantum coherence and all stored data
8. **File Monitoring**: Real file integrity checking with quantum-secured checksums stored in PostgreSQL

**Key Innovation**: The algorithm creates a quantum matrix that BREAKS upon collapse (attack) BUT the data 
is ALWAYS PRESERVED through entropy-based secure storage. The quantum state resets, but information persists.

This demonstrates quantum security with classical data persistence - the perfect hybrid cybersecurity system.
""")

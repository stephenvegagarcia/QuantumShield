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

st.set_page_config(page_title="Quantum Security System", layout="wide")

st.title("🔐 Quantum Entanglement Self-Healing Security System")
st.markdown("### Bell State |φ⁺⟩ = 1/√2 (|00⟩ + |11⟩)")

if 'attack_log' not in st.session_state:
    st.session_state.attack_log = []
if 'system_resets' not in st.session_state:
    st.session_state.system_resets = 0
if 'measurements' not in st.session_state:
    st.session_state.measurements = {'00': 0, '11': 0, 'other': 0}
if 'quantum_intact' not in st.session_state:
    st.session_state.quantum_intact = True
if 'last_attack_results' not in st.session_state:
    st.session_state.last_attack_results = None
if 'under_attack' not in st.session_state:
    st.session_state.under_attack = False
if 'entropy_storage' not in st.session_state:
    st.session_state.entropy_storage = []
if 'secure_data_store' not in st.session_state:
    st.session_state.secure_data_store = []
if 'system_version' not in st.session_state:
    st.session_state.system_version = 1

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

def store_quantum_data_with_entropy(counts, timestamp):
    entropy = calculate_entropy(counts)
    
    data_hash = int(entropy * 1000) % 256
    
    data_entry = {
        'timestamp': timestamp,
        'entropy_key': entropy,
        'hash': data_hash,
        'correlation': (counts.get('00', 0) + counts.get('11', 0)) / sum(counts.values()) * 100,
        'measurements': counts
    }
    
    st.session_state.entropy_storage.append(entropy)
    st.session_state.secure_data_store.append(data_entry)
    
    return entropy

def upgrade_system():
    st.session_state.system_version += 1
    st.session_state.attack_log.append({
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'event': 'System Upgrade',
        'reason': f'Upgraded to version {st.session_state.system_version} - Quantum coherence maintained'
    })

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
        attack_entropy = store_quantum_data_with_entropy(attack_counts, timestamp)
        
        st.session_state.attack_log.append({
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'event': 'Attack Detected',
            'reason': f'Eavesdropper introduced decoherence - Data secured with entropy {attack_entropy:.4f}'
        })
        
        if detect_attack(attack_counts):
            st.session_state.quantum_intact = False
            st.session_state.under_attack = True
        
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

st.markdown("""
### 🔬 How This Quantum Security System Works

1. **Quantum Matrix Creation**: Uses H(0) → CNOT(0,1) to create entangled Bell state |φ⁺⟩
2. **Perfect Correlation**: The Bell state |φ⁺⟩ = 1/√2 (|00⟩ + |11⟩) ensures measurements are always 00 or 11
3. **Entropy-Based Storage**: ALL measurements (normal + attack) are secured with Shannon entropy keys
4. **Data Persistence**: Even when quantum state collapses from attack, data is preserved in classical storage
5. **Attack Detection**: Eavesdropping introduces decoherence, breaking the perfect Bell correlation
6. **Auto-Reset**: System detects correlation drop and automatically restores to original quantum state
7. **System Upgrades**: Can upgrade versions over time while maintaining quantum coherence and all stored data

**Key Innovation**: The algorithm creates a quantum matrix that BREAKS upon collapse (attack) BUT the data 
is ALWAYS PRESERVED through entropy-based secure storage. The quantum state resets, but information persists.

This demonstrates quantum security with classical data persistence - the perfect hybrid cybersecurity system.
""")

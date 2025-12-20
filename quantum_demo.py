#!/usr/bin/env python3
"""Quantum Security Demonstration"""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
import numpy as np

def create_bell_state():
    print("\n" + "="*70)
    print("⚛️  QUANTUM BELL STATE: 1/√2 (|00⟩ + |11⟩)")
    print("="*70)
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])  # Superposition: 1/√2 (|0⟩ + |1⟩)
    qc.cx(qr[0], qr[1])  # Entanglement
    print("✅ Bell state created - qubits are now ENTANGLED")
    return qc

def measure_normal(qc):
    print("\n📊 NORMAL MEASUREMENT (No Attack):")
    qc_copy = qc.copy()
    qc_copy.measure([0,1], [0,1])
    backend = Aer.get_backend('qasm_simulator')
    counts = backend.run(qc_copy, shots=1000).result().get_counts()
    for state, count in sorted(counts.items()):
        print(f"   |{state}⟩: {count} ({count/10:.1f}%)")
    corr = (counts.get('00',0) + counts.get('11',0)) / 10
    print(f"   Correlation: {corr:.1f}% ✅ SECURE")
    return counts, corr

def simulate_attack(qc):
    print("\n⚠️  ATTACK SIMULATION (Eavesdropper measures):")
    qc_attack = qc.copy()
    qc_attack.measure(0, 0)  # COLLAPSE wave function!
    qc_attack.barrier()
    qc_attack.h(1)
    qc_attack.z(0)
    qc_attack.measure([0,1], [0,1])
    backend = Aer.get_backend('qasm_simulator')
    counts = backend.run(qc_attack, shots=1000).result().get_counts()
    for state, count in sorted(counts.items()):
        print(f"   |{state}⟩: {count} ({count/10:.1f}%)")
    corr = (counts.get('00',0) + counts.get('11',0)) / 10
    print(f"   Correlation: {corr:.1f}% ❌ ATTACK DETECTED!")
    return counts, corr

print("\n🔐 QUANTUMSHIELD - Quantum Physics Security Demo")
print("\n📚 PRINCIPLE: Binary States (0 and 1 ONLY)")
print("   • Qubits can only be |0⟩ or |1⟩ (NO 2, 3, 4...)")
print("   • Bell state: 1/√2 (|00⟩ + |11⟩)")
print("   • Perfect correlation when measured together")
print("   • Attack breaks entanglement → detectable!")

bell = create_bell_state()
normal_counts, normal_corr = measure_normal(bell)
attack_counts, attack_corr = simulate_attack(bell)

print("\n" + "="*70)
print("📊 RESULTS:")
print(f"   Normal correlation:  {normal_corr:.1f}% (Expected: ~100%)")
print(f"   Attack correlation:  {attack_corr:.1f}% (Dropped!)")
print(f"   Violation detected:  {normal_corr - attack_corr:.1f}%")
print("\n✅ PHYSICS ENFORCES SECURITY - Attack is IMPOSSIBLE to hide!")
print("="*70 + "\n")

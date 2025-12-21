#!/usr/bin/env python3
"""
Quantum Recovery Simulation
Demonstrates quantum error correction using Bell states with QuTiP
"""
import qutip as qt
import numpy as np

# Manual Gates
H = qt.Qobj([[1, 1], [1, -1]]) / np.sqrt(2)
X = qt.sigmax()
Z = qt.sigmaz()
I = qt.qeye(2)

def simulate_recovery():
    """
    Simulates quantum attack and recovery on a Bell state.
    
    Returns:
        tuple: (attacked_correlation, recovered_correlation)
            - attacked_correlation: Correlation percentage after attack
            - recovered_correlation: Correlation percentage after recovery
    """
    # 1. Setup: Perfect Bell State (|00> + |11>)
    bell = (qt.tensor(qt.basis(2,0), qt.basis(2,0)) + qt.tensor(qt.basis(2,1), qt.basis(2,1))).unit()
    rho = bell * bell.dag()

    # 2. THE ATTACK (The "Negative" influence)
    # Eve measures and Bob's qubit gets flipped/shifted
    # We represent this as a Phase Flip (Z) and Bit Flip (X)
    noise = qt.tensor(Z, X)
    rho_attacked = noise * rho * noise.dag()

    # 3. THE REVERSAL (The "Correction" logic)
    # Alice and Bob detect the 'negative' shift. 
    # To 'hack' it back, they apply the inverse operators.
    # Since X*X=I and Z*Z=I, this reverses the attack.
    correction = qt.tensor(Z, X) 
    rho_recovered = correction * rho_attacked * correction.dag()

    # 4. Measuring Results
    def get_corr(state):
        P_sync = qt.tensor(qt.basis(2,0)*qt.basis(2,0).dag(), qt.basis(2,0)*qt.basis(2,0).dag()) + \
                 qt.tensor(qt.basis(2,1)*qt.basis(2,1).dag(), qt.basis(2,1)*qt.basis(2,1).dag())
        return (P_sync * state).tr().real * 100

    return get_corr(rho_attacked), get_corr(rho_recovered)

def main():
    """Execute the quantum recovery simulation and display results."""
    # Execute
    attacked_val, recovered_val = simulate_recovery()

    print(f"Correlation after Attack (Negative): {attacked_val:.1f}%")
    print(f"Correlation after Reverse/Reset (Positive): {recovered_val:.1f}%")

if __name__ == "__main__":
    main()

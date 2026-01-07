"""
Quantum Gate Visualization Module for Streamlit UI
Provides matplotlib-based visualizations of quantum gates and states
"""
import numpy as np
import matplotlib.pyplot as plt
from qutip import ket, tensor, ptrace, entropy_vn, sigmaz, sigmax, sigmay, qeye
from qutip.qip.operations import hadamard_transform, phasegate
import subprocess
import os


class QuantumGateVisualizer:
    """Visualizer for quantum gates and their effects"""
    
    def __init__(self):
        self.H = hadamard_transform()   # Hadamard gate
        self.X = sigmax()               # NOT/Pauli-X
        self.Y = sigmay()               # Pauli-Y
        self.Z = sigmaz()               # Pauli-Z
        self.S = phasegate(np.pi / 2)   # S gate (Phase π/2)
        self.P = phasegate(np.pi / 4)   # P gate (π/4 gate)
        self.I = qeye(2)                # Identity
        
    def CNOT(self, control_qubit=0, target_qubit=1):
        """CNOT gate for 2-qubit system."""
        P0 = ket('0') * ket('0').dag()
        P1 = ket('1') * ket('1').dag()
        
        if control_qubit == 0 and target_qubit == 1:
            return tensor(P0, self.I) + tensor(P1, self.X)
        elif control_qubit == 1 and target_qubit == 0:
            return tensor(self.I, P0) + tensor(self.X, P1)
        else:
            raise ValueError("control_qubit and target_qubit must be different in {0,1}.")
    
    def create_bell_state(self):
        """Create Bell state using CNOT: CNOT(H⊗I)|00⟩"""
        psi_0 = tensor(ket('0'), ket('0'))
        HI = tensor(self.H, self.I)
        psi_plus = self.CNOT(0, 1) * HI * psi_0
        return psi_plus.unit()
    
    def apply_gate(self, gate_type, state=None):
        """Apply a specific gate to a state"""
        if state is None:
            state = tensor(ket('0'), ket('0'))
        
        if gate_type == "BELL":
            return self.create_bell_state()
        elif gate_type == "HXXH":
            HH = tensor(self.H, self.H)
            return HH * state
        elif gate_type == "CNOT":
            HI = tensor(self.H, self.I)
            return self.CNOT(0, 1) * HI * state
        elif gate_type == "CZ":
            HH = tensor(self.H, self.H)
            P0 = ket('0') * ket('0').dag()
            P1 = ket('1') * ket('1').dag()
            CZ = tensor(P0, self.I) + tensor(P1, self.Z)
            return CZ * HH * state
        elif gate_type == "X":
            return tensor(self.X, self.I) * state
        elif gate_type == "Y":
            return tensor(self.Y, self.I) * state
        elif gate_type == "Z":
            return tensor(self.Z, self.I) * state
        elif gate_type == "H":
            return tensor(self.H, self.I) * state
        else:
            return state
    
    def calculate_entropy(self, state, apply_noise=False, noise_level=0.3):
        """Calculate von Neumann entropy of the reduced density matrix"""
        if apply_noise:
            noise_x = noise_level * tensor(self.X, self.I) / 3
            noise_z = noise_level * tensor(self.Z, self.I) / 3
            noise_y = noise_level * tensor(self.Y, self.I) / 3
            noise_op = (1 - noise_level) * tensor(qeye(2), qeye(2)) + noise_x + noise_z + noise_y
        else:
            noise_level = 0.01
            noise_op = (1 - noise_level) * tensor(qeye(2), qeye(2)) + noise_level * tensor(self.Z, qeye(2))
        
        rho = noise_op * state * state.dag() * noise_op.dag()
        rho = rho / rho.tr()  # Normalize
        
        entropy = entropy_vn(ptrace(rho, 0))
        return entropy
    
    def plot_gate_matrix(self, gate_type):
        """Plot the matrix representation of a quantum gate"""
        gates = {
            "H": self.H,
            "X": self.X,
            "Y": self.Y,
            "Z": self.Z,
            "S": self.S,
            "P": self.P,
            "I": self.I,
        }
        
        if gate_type not in gates:
            return None
        
        gate = gates[gate_type]
        matrix = gate.full()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        
        # Real part
        im1 = ax1.imshow(np.real(matrix), cmap='RdBu', vmin=-1, vmax=1)
        ax1.set_title(f'{gate_type} Gate - Real Part')
        ax1.set_xlabel('Column')
        ax1.set_ylabel('Row')
        plt.colorbar(im1, ax=ax1)
        
        # Imaginary part
        im2 = ax2.imshow(np.imag(matrix), cmap='RdBu', vmin=-1, vmax=1)
        ax2.set_title(f'{gate_type} Gate - Imaginary Part')
        ax2.set_xlabel('Column')
        ax2.set_ylabel('Row')
        plt.colorbar(im2, ax=ax2)
        
        # Add values as text
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                real_val = np.real(matrix[i, j])
                imag_val = np.imag(matrix[i, j])
                if abs(real_val) > 0.01:
                    ax1.text(j, i, f'{real_val:.2f}', ha='center', va='center', color='white' if abs(real_val) > 0.5 else 'black')
                if abs(imag_val) > 0.01:
                    ax2.text(j, i, f'{imag_val:.2f}', ha='center', va='center', color='white' if abs(imag_val) > 0.5 else 'black')
        
        plt.tight_layout()
        return fig
    
    def plot_state_comparison(self, gate_types, apply_noise=False):
        """Plot comparison of different gate effects on quantum states"""
        fig, axes = plt.subplots(2, len(gate_types), figsize=(4*len(gate_types), 8))
        if len(gate_types) == 1:
            axes = axes.reshape(-1, 1)
        
        for idx, gate_type in enumerate(gate_types):
            state = self.apply_gate(gate_type)
            entropy = self.calculate_entropy(state, apply_noise=apply_noise)
            
            # Get density matrix
            rho = state * state.dag()
            density = rho.full()
            
            # Plot real part
            im1 = axes[0, idx].imshow(np.real(density), cmap='viridis', vmin=0, vmax=1)
            axes[0, idx].set_title(f'{gate_type}\nEntropy: {entropy:.4f}')
            axes[0, idx].set_xlabel('Column')
            axes[0, idx].set_ylabel('Row')
            plt.colorbar(im1, ax=axes[0, idx])
            
            # Plot state vector amplitudes
            state_vec = state.full().flatten()
            basis_states = ['|00⟩', '|01⟩', '|10⟩', '|11⟩']
            amplitudes = np.abs(state_vec)**2
            
            axes[1, idx].bar(basis_states, amplitudes, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
            axes[1, idx].set_title(f'State Probabilities')
            axes[1, idx].set_ylabel('Probability')
            axes[1, idx].set_ylim([0, 1])
            axes[1, idx].grid(True, alpha=0.3)
            
            # Add probability values on bars
            for i, (basis, amp) in enumerate(zip(basis_states, amplitudes)):
                if amp > 0.01:
                    axes[1, idx].text(i, amp + 0.02, f'{amp:.3f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        return fig
    
    def launch_interactive_visualizer(self):
        """Launch the interactive pygame visualizer in a subprocess"""
        script_path = os.path.join(os.path.dirname(__file__), 'quantum_gate_visualizer.py')
        try:
            # Launch in background
            subprocess.Popen(['python', script_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            return True, "Interactive visualizer launched successfully!"
        except Exception as e:
            return False, f"Error launching visualizer: {str(e)}"


def get_gate_description(gate_type):
    """Get description of a quantum gate"""
    descriptions = {
        "H": "**Hadamard Gate**: Creates superposition |0⟩ → 1/√2(|0⟩ + |1⟩)",
        "X": "**Pauli-X Gate**: Quantum NOT gate, flips |0⟩ ↔ |1⟩",
        "Y": "**Pauli-Y Gate**: Rotation around Y-axis with phase flip",
        "Z": "**Pauli-Z Gate**: Phase flip |1⟩ → -|1⟩, leaves |0⟩ unchanged",
        "S": "**S Gate**: Phase gate (π/2), adds 90° phase to |1⟩",
        "P": "**P Gate**: Phase gate (π/4), adds 45° phase to |1⟩",
        "BELL": "**Bell State**: Maximally entangled state 1/√2(|00⟩ + |11⟩)",
        "HXXH": "**H⊗H Operation**: Double Hadamard, creates 4-state superposition",
        "CNOT": "**CNOT Gate**: Controlled-NOT, creates entanglement",
        "CZ": "**CZ Gate**: Controlled-Z, phase-based entanglement",
    }
    return descriptions.get(gate_type, "Quantum gate operation")

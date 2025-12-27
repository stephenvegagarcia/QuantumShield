#!/usr/bin/env python3
"""
Quantum Gate Defender - Interactive Visualization
Demonstrates quantum gates and entanglement using pygame and qutip
"""
import pygame
import numpy as np
from qutip import ket, tensor, ptrace, entropy_vn, sigmaz, sigmax, sigmay, qeye
from qutip.qip.operations import hadamard_transform, phasegate
import random

# --- 1. Enhanced Quantum Gate Library ---
class QuantumGateSystem:
    def __init__(self):
        self.H = hadamard_transform()   # Hadamard gate
        self.X = sigmax()               # NOT/Pauli-X
        self.Y = sigmay()               # Pauli-Y
        self.Z = sigmaz()               # Pauli-Z
        self.S = phasegate(np.pi / 2)   # S gate (Phase π/2)
        self.P = phasegate(np.pi / 4)   # P gate (π/4 gate)
        self.I = qeye(2)                # Identity

    def CNOT(self, control_qubit, target_qubit, num_qubits=2):
        """CNOT gate for multi-qubit system (2-qubit supported)."""
        if num_qubits != 2:
            return tensor(self.I, self.I)

        P0 = ket('0') * ket('0').dag()
        P1 = ket('1') * ket('1').dag()

        if control_qubit == 0 and target_qubit == 1:
            # |0><0| ⊗ I + |1><1| ⊗ X
            return tensor(P0, self.I) + tensor(P1, self.X)
        elif control_qubit == 1 and target_qubit == 0:
            # I ⊗ |0><0| + X ⊗ |1><1|
            return tensor(self.I, P0) + tensor(self.X, P1)
        else:
            raise ValueError("control_qubit and target_qubit must be different in {0,1}.")

    def CZ(self, num_qubits=2):
        """Controlled-Z gate: |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ Z"""
        if num_qubits != 2:
            return tensor(self.I, self.I)
        P0 = ket('0') * ket('0').dag()
        P1 = ket('1') * ket('1').dag()
        return tensor(P0, self.I) + tensor(P1, self.Z)

    def HXXH(self, state):
        """Apply H⊗H to a 2-qubit state."""
        HH = tensor(self.H, self.H)
        return HH * state

# --- 2. The Bell Shield with Gate Operations ---
class QuantumDefender:
    def __init__(self):
        self.message = "HELLO WORLD"
        self.shield_active = False
        self.attack_active = False
        self.gate_mode = "BELL"  # BELL, HXXH, CNOT, CZ, PAULI, PHASE
        self.gates = QuantumGateSystem()
        self.gate_sequence = []

    def create_bell_state(self):
        """Create Bell state using CNOT:  CNOT(H⊗I)|00⟩"""
        psi_0 = tensor(ket('0'), ket('0'))
        HI = tensor(self.gates.H, self.gates.I)
        psi_plus = self.gates.CNOT(0, 1) * HI * psi_0
        return psi_plus.unit()

    def apply_defense_gates(self, state, mode):
        """Apply different gate combinations for defense."""
        if mode == "HXXH":
            return self.gates.HXXH(state)
        elif mode == "CNOT":
            HI = tensor(self.gates.H, self.gates.I)
            return self.gates.CNOT(0, 1) * HI * state
        elif mode == "CZ":
            HH = tensor(self.gates.H, self.gates.H)
            return self.gates.CZ() * HH * state
        elif mode == "PAULI":
            pauli_ops = [
                tensor(self.gates.X, self.gates.I),
                tensor(self.gates.Y, self.gates.I),
                tensor(self.gates.Z, self.gates.I),
                tensor(self.gates.I, self.gates.X),
            ]
            op = random.choice(pauli_ops)
            return op * state
        elif mode == "PHASE":
            SP = tensor(self.gates.S, self.gates.P)
            return SP * state
        else:  # BELL
            return self.create_bell_state()

    def calculate_defense(self, entropy, mode):
        """Calculate defense status based on gate mode."""
        thresholds = {
            "BELL": 0.02,
            "HXXH": 0.05,
            "CNOT": 0.03,
            "CZ": 0.04,
            "PAULI": 0.08,
            "PHASE": 0.06,
        }

        threshold = thresholds.get(mode, 0.02)

        if self.shield_active:
            if entropy > threshold:
                return f"⚡ {mode} DEFLECTED ⚡", (0, 255, 255)  # Cyan
            return f"✓ {mode} STABLE", (0, 255, 100)  # Green
        return "⚠ UNPROTECTED", (200, 200, 200)  # Gray

def main():
    """Main function to run the quantum gate visualizer."""
    # --- 3. Simulation Setup ---
    WIDTH, HEIGHT = 1100, 750
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Quantum Gate Defender - QuantumShield")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Courier", 18, bold=True)
    font_small = pygame.font.SysFont("Courier", 14)
    defender = QuantumDefender()

    # 4D Hypercube Setup
    points = [
        np.array(
            [
                [1 if i & 1 else -1],
                [1 if i & 2 else -1],
                [1 if i & 4 else -1],
                [1 if i & 8 else -1],
            ],
            dtype=float,
        )
        for i in range(16)
    ]

    angle = 0
    running = True
    gate_colors = {
        "BELL": (100, 150, 255),
        "HXXH": (255, 200, 0),
        "CNOT": (255, 100, 200),
        "CZ": (150, 0, 255),
        "PAULI": (255, 50, 50),
        "PHASE": (0, 255, 200),
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Toggle Shield
                    defender.shield_active = not defender.shield_active
                if event.key == pygame.K_a:  # Toggle Attack
                    defender.attack_active = not defender.attack_active
                if event.key == pygame.K_1:  # Bell State
                    defender.gate_mode = "BELL"
                if event.key == pygame.K_2:  # H⊗H⊗H⊗H mode
                    defender.gate_mode = "HXXH"
                if event.key == pygame.K_3:  # CNOT mode
                    defender.gate_mode = "CNOT"
                if event.key == pygame.K_4:  # CZ mode
                    defender.gate_mode = "CZ"
                if event.key == pygame.K_5:  # Pauli mode
                    defender.gate_mode = "PAULI"
                if event.key == pygame.K_6:  # S/P Phase gates
                    defender.gate_mode = "PHASE"

        screen.fill((5, 0, 20))

        # --- Quantum Physics Engine ---
        base_state = tensor(ket('0'), ket('0'))

        # Apply defense gates
        psi_shield = defender.apply_defense_gates(base_state, defender.gate_mode)

        # Simulate Attack with Pauli noise
        if defender.attack_active:
            noise_level = 0.3 + 0.4 * random.random()
            noise_x = noise_level * tensor(defender.gates.X, defender.gates.I) / 3
            noise_z = noise_level * tensor(defender.gates.Z, defender.gates.I) / 3
            noise_y = noise_level * tensor(defender.gates.Y, defender.gates.I) / 3
            noise_op = (1 - noise_level) * tensor(qeye(2), qeye(2)) + noise_x + noise_z + noise_y
        else:
            noise_level = 0.01
            noise_op = (1 - noise_level) * tensor(qeye(2), qeye(2)) + noise_level * tensor(defender.gates.Z, qeye(2))

        rho = noise_op * psi_shield * psi_shield.dag() * noise_op.dag()
        rho = rho / rho.tr()  # Normalize density matrix

        entropy = entropy_vn(ptrace(rho, 0))
        status_text, current_color = defender.calculate_defense(entropy, defender.gate_mode)

        # --- 4D Visuals: The Quantum Shield Tesseract ---
        a = angle
        w_dist = 3.0 if defender.shield_active else 4.5

        # Rotation influenced by gate mode
        speed_mult = 1.5 if defender.gate_mode == "HXXH" else 1.0

        rot = np.array(
            [
                [np.cos(a), 0, 0, -np.sin(a)],
                [0, np.cos(a), -np.sin(a), 0],
                [0, np.sin(a), np.cos(a), 0],
                [np.sin(a), 0, 0, np.cos(a)],
            ]
        )

        projected = []
        for p in points:
            p_rotated = np.dot(rot, p)
            z = 1 / (w_dist - p_rotated[3][0])
            p2d = np.dot(np.array([[z, 0, 0, 0], [0, z, 0, 0]]), p_rotated)
            projected.append(
                (
                    int(p2d[0][0] * 150 + WIDTH // 2),
                    int(p2d[1][0] * 150 + HEIGHT // 2),
                )
            )

        # Draw with gate-specific color
        display_color = gate_colors.get(defender.gate_mode, current_color) if not defender.attack_active else current_color
        line_width = 3 if defender.shield_active else 1

        for i in range(16):
            for j in range(i + 1, 16):
                if bin(i ^ j).count("1") == 1:
                    pygame.draw.line(screen, display_color, projected[i], projected[j], line_width)
            pygame.draw.circle(screen, display_color, projected[i], 4 if defender.shield_active else 2)

        # --- Dashboard ---
        panel_height = 320
        pygame.draw.rect(screen, (0, 10, 30), (20, 20, 650, panel_height))
        pygame.draw.rect(screen, current_color, (20, 20, 650, panel_height), 3)

        if defender.attack_active and not defender.shield_active:
            display_msg = "!! DATA BREACH !!"
        elif defender.attack_active and defender.shield_active:
            display_msg = "".join(c if random.random() > entropy else "_" for c in defender.message)
        else:
            display_msg = defender.message

        ui = [
            f"═══ QUANTUM GATE DEFENDER ═══",
            f"CORE DATA: [ {display_msg} ]",
            f"",
            f"GATE MODE: {defender.gate_mode}",
            f"SHIELD:  {'[████ ON ████]' if defender.shield_active else '[---- OFF ----]'}",
            f"ATTACK:  {'[!!! ACTIVE !!!]' if defender.attack_active else '[   NONE    ]'}",
            f"",
            f"ENTROPY S(ρ): {entropy:.6f}",
            f"STATUS: {status_text}",
        ]

        for i, line in enumerate(ui):
            screen.blit(font.render(line, True, current_color if i != 0 else (255, 255, 100)), (40, 35 + (i * 30)))

        # Gate descriptions
        gate_panel_y = 360
        pygame.draw.rect(screen, (10, 0, 20), (20, gate_panel_y, 650, 180))
        pygame.draw.rect(screen, (100, 100, 150), (20, gate_panel_y, 650, 180), 2)

        gate_info = [
            "[1] BELL   : CNOT(H⊗I)|00⟩",
            "[2] HXXH   : H⊗H Superposition",
            "[3] CNOT   : Controlled-NOT Entangle",
            "[4] CZ     : Controlled-Z Phase",
            "[5] PAULI  : X,Y,Z Randomization",
            "[6] PHASE  : S(π/2) & P(π/4) Gates",
        ]

        for i, line in enumerate(gate_info):
            gate_name = line.split()[1]  # e.g., "BELL", "HXXH", ...
            color = gate_colors.get(gate_name, (150, 150, 150))
            screen.blit(font_small.render(line, True, color), (40, gate_panel_y + 20 + i * 25))

        controls = "[S] Shield | [A] Attack | [1-6] Gate Modes"
        screen.blit(font_small.render(controls, True, (150, 150, 150)), (20, HEIGHT - 30))

        angle += 0.01 * speed_mult
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

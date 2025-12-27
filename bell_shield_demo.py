#!/usr/bin/env python3
"""
Bell Shield Quantum Visualization Demo
Interactive visualization of quantum entanglement-based security using Bell states
"""
import pygame
import numpy as np
from qutip import ket, tensor, ptrace, entropy_vn, sigmaz, qeye
import random

# --- 1. The Bell Shield Logic ---
class QuantumDefender:
    def __init__(self):
        self.message = "HELLO WORLD"
        self.shield_active = False
        self.attack_active = False
        self.fidelity = 1.0
        
    def calculate_defense(self, entropy):
        # The Bell Shield (1/sqrt(2) * |00> + |11>)
        # If the shield is on, we reject any measurement that isn't perfectly correlated
        if self.shield_active:
            if entropy > 0.02: # Extremely sensitive defense
                return "SHIELD DEFLECTED ATTACK", (0, 255, 255) # Cyan
            return "SHIELD STABLE", (0, 100, 255)
        return "UNPROTECTED", (200, 200, 200)

# --- 2. Simulation Setup ---
WIDTH, HEIGHT = 950, 700
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier", 20, bold=True)
defender = QuantumDefender()

# 4D Hypercube Setup
points = [np.array([[1 if i & 1 else -1], [1 if i & 2 else -1], 
                    [1 if i & 4 else -1], [1 if i & 8 else -1]], dtype=float) for i in range(16)]

angle = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: # Toggle Bell Shield (00 + 11)
                defender.shield_active = not defender.shield_active
            if event.key == pygame.K_a: # Toggle Attack
                defender.attack_active = not defender.attack_active

    screen.fill((5, 0, 20))
    
    # --- Quantum Physics Engine ---
    # Vault Base State: |00> + |11>
    psi_shield = (tensor(ket('0'), ket('0')) + tensor(ket('1'), ket('1'))).unit()
    
    # Simulate Attack Pressure
    noise_level = 0.5 * random.random() if defender.attack_active else 0.02
    noise_op = (1 - noise_level) * qeye([2, 2]) + noise_level * tensor(sigmaz(), qeye(2))
    rho = noise_op * psi_shield * psi_shield.dag() * noise_op.dag()
    
    entropy = entropy_vn(ptrace(rho, 0))
    status_text, current_color = defender.calculate_defense(entropy)

    # --- 4D Visuals: The Bell Projection ---
    a = angle
    # The Tesseract becomes a "Shield Wall" if defense is active
    w_dist = 4.0 if not defender.shield_active else 2.5
    
    rot = np.array([[np.cos(a), 0, 0, -np.sin(a)], [0, np.cos(a), -np.sin(a), 0],
                    [0, np.sin(a), np.cos(a), 0], [np.sin(a), 0, 0, np.cos(a)]])

    projected = []
    for p in points:
        p_rotated = np.dot(rot, p)
        z = 1 / (w_dist - p_rotated[3][0])
        p2d = np.dot(np.array([[z, 0, 0, 0], [0, z, 0, 0]]), p_rotated)
        projected.append((int(p2d[0][0] * 1500 + WIDTH // 2), 
                          int(p2d[1][0] * 1500 + HEIGHT // 2)))

    # Draw Logic: If shielded, draw double lines for "Quantum thickness"
    for i in range(16):
        for j in range(i + 1, 16):
            if bin(i ^ j).count('1') == 1:
                pygame.draw.line(screen, current_color, projected[i], projected[j], 2 if defender.shield_active else 1)

    # --- Dashboard ---
    pygame.draw.rect(screen, (0, 10, 30), (20, 20, 520, 240))
    pygame.draw.rect(screen, current_color, (20, 20, 520, 240), 2)
    
    # Logic: "HELLO WORLD" is only visible if Shield is holding or Attack is off
    if defender.attack_active and not defender.shield_active:
        display_msg = "!! CRITICAL LEAK !!"
    elif defender.attack_active and defender.shield_active:
        display_msg = "H_L_O_W_R_D (PHASED)"
    else:
        display_msg = defender.message

    ui = [
        f"CORE DATA: [ {display_msg} ]",
        f"BELL SHIELD (00+11): {'[ ON ]' if defender.shield_active else '[ OFF ]'}",
        f"ATTACK STATUS: {'[ BREACHING ]' if defender.attack_active else '[ NONE ]'}",
        f"ENTROPY (S): {entropy:.4f}",
        f"DEFENSE STATUS: {status_text}"
    ]
    
    for i, line in enumerate(ui):
        screen.blit(font.render(line, True, current_color), (40, 40 + (i * 35)))

    screen.blit(font.render("[S] Bell Shield | [A] Attack Mode", True, (150, 150, 150)), (20, HEIGHT - 40))

    angle += 0.01
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# Quantum Security System

## Overview

This project is a Quantum Entanglement Self-Healing Security System built with Streamlit. It leverages quantum computing principles, specifically Bell state entanglement (|φ⁺⟩ = 1/√2 (|00⟩ + |11⟩)), to create a security monitoring and self-healing system with persistent file protection. The application uses IBM's Qiskit framework to simulate quantum circuits and detect security anomalies through quantum state measurements. The system maintains entropy measurements, tracks attack patterns, implements self-healing mechanisms, and monitors real file integrity. All security data persists to PostgreSQL, ensuring continuity across sessions.

## Defense-in-Depth Philosophy: The Castle Structure

**This system is designed as a secondary defense layer - like a castle protecting what's inside.**

### Not a Primary Security System
This system is **not meant to replace** your device's built-in security features:
- Phone operating system security (iOS/Android sandboxing)
- CPU-level security features (Intel SGX, ARM TrustZone)
- Antivirus software or endpoint protection
- Firewall and network security

### Backup Security Layer
Instead, this system serves as a **fallback protection layer** that activates when primary defenses fail:
- **If your device's OS security is compromised** → This system detects file tampering
- **If your CPU security features fail** → This system monitors malicious processes
- **If your primary antivirus misses a threat** → This system catches suspicious behavior
- **If ransomware bypasses device protection** → This system creates emergency backups

### The Castle Analogy
Think of it like medieval castle defenses:
1. **Primary Defenses** (walls, moat) = Your device's built-in security
2. **Secondary Defenses** (guard towers, backup gates) = This quantum security system
3. **Last Resort** (keep, emergency escape routes) = File backups and automated responses

**Key Principle:** When the first wall falls, the castle still stands. When your device's security fails, this system provides an additional layer of protection to minimize damage and enable recovery.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with wide layout configuration
- **Visualization Components**: 
  - Matplotlib for quantum state visualizations (Bloch sphere, state city plots)
  - Plotly for interactive graphs and real-time monitoring
  - Custom quantum circuit diagrams
- **State Management**: Streamlit session state for persistent data across reruns, including:
  - Attack logs and system reset counters
  - Measurement statistics (00, 11, and anomalous states)
  - Quantum integrity status flags
  - Entropy storage for security analysis
  - Secure data storage mechanisms
  - System versioning for recovery points

### Backend Architecture
- **Quantum Computing Layer**: 
  - Qiskit framework for quantum circuit creation and simulation
  - Aer simulator backend for executing quantum circuits
  - Quantum registers (2-qubit system) and classical measurement registers
  - Bell state generation using Hadamard and CNOT gates
- **Security Monitoring**:
  - Entropy calculation engine for detecting quantum state anomalies
  - Attack detection through measurement distribution analysis
  - Self-healing mechanisms triggered by quantum decoherence detection
  - Real file integrity monitoring with SHA-256 checksums
- **Database Layer**:
  - PostgreSQL database for persistent storage
  - SQLAlchemy ORM for database operations
  - Tables: system_state, security_events, quantum_measurements, monitored_files
  - All quantum data and security events persisted across sessions
- **Data Processing**: NumPy for numerical computations and state vector analysis

### Core Design Patterns
- **Quantum State Factory**: `create_bell_state()` function generates maximally entangled two-qubit systems as security baseline
- **Stateful Security Monitor**: Session-based tracking of system integrity across multiple measurements
- **Entropy-Based Anomaly Detection**: Mathematical entropy calculations on measurement outcomes to identify attacks
- **Self-Healing Protocol**: Automatic system resets when quantum correlations deviate from expected Bell state properties

## External Dependencies

### Quantum Computing Framework
- **Qiskit**: IBM's quantum computing SDK for circuit creation, simulation, and state analysis
- **Qiskit Aer**: High-performance quantum circuit simulator backend
- **Qiskit Quantum Info**: Statevector operations and quantum state representations

### Visualization Libraries
- **Matplotlib**: Static quantum state visualizations (Bloch sphere, density matrices)
- **Plotly**: Interactive real-time security monitoring dashboards

### Web Framework
- **Streamlit**: Full-stack web application framework with reactive state management

### Scientific Computing
- **NumPy**: Array operations, numerical analysis, and quantum probability calculations

### Standard Library
- **datetime**: Timestamp generation for attack logs and system events
- **time**: Timing operations for attack simulations and monitoring intervals
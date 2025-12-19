# 🔐 QuantumShield - Quantum Entanglement Self-Healing Security System

A quantum computing-based security monitoring and self-healing system that leverages Bell state entanglement for detecting and responding to security threats.

## Overview

QuantumShield is a secondary defense layer security system built with quantum computing principles. It uses IBM's Qiskit framework to simulate quantum circuits and detect security anomalies through quantum state measurements. The system provides:

- **Quantum Entanglement Security**: Bell State implementation using quantum circuits
- **Attack Detection & Self-Healing**: Automatic detection and recovery from security breaches
- **File Integrity Monitoring**: Real-time monitoring of important files
- **Malware Detection**: Process scanning for suspicious activity
- **Ransomware Protection**: Detection and prevention of ransomware attacks
- **Persistent Data Storage**: All security data stored in PostgreSQL/SQLite

## Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/stephenvegagarcia/QuantumShield.git
   cd QuantumShield
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```
   
   Or install manually:
   ```bash
   pip install flask numpy qiskit qiskit-aer matplotlib psutil sqlalchemy streamlit plotly pylatexenc psycopg2-binary
   ```

### Running the Application

The easiest way to run QuantumShield is using the `main.py` entry point:

```bash
# Run Streamlit app (default, recommended)
python main.py

# Or explicitly choose Streamlit
python main.py streamlit

# Run Flask app instead
python main.py flask

# Show help
python main.py help
```

#### Streamlit Interface (Recommended)

The Streamlit interface provides an interactive, real-time dashboard:

```bash
python main.py streamlit
```

Then open your browser to: **http://localhost:8501**

#### Flask Interface

For a traditional web application experience:

```bash
python main.py flask
```

Then open your browser to: **http://localhost:5000**

### Database Configuration

By default, the application uses SQLite (`quantum_security.db`) for data persistence.

For PostgreSQL (recommended for production):

```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
python main.py
```

## Features

### 🔬 Quantum Security Layer
- Bell State entanglement: |φ⁺⟩ = 1/√2 (|00⟩ + |11⟩)
- Quantum circuit simulation using Qiskit
- Entropy-based anomaly detection
- Automatic self-healing when attacks are detected

### 🛡️ File Protection
- Real-time file integrity monitoring
- Quantum-secured checksums
- Automatic backup creation
- Tamper detection and alerts

### 🦠 Threat Detection
- Process-based malware detection
- Ransomware activity monitoring
- Suspicious behavior analysis
- Automated threat response

### 📊 Monitoring Dashboard
- Real-time quantum state visualization
- Bloch sphere and state city plots
- Attack logs and system events
- Measurement statistics and entropy tracking

## Defense-in-Depth Philosophy

**This system is a secondary defense layer** - like a castle protecting what's inside.

### Not a Primary Security System
This does **not replace** your device's built-in security:
- ❌ Operating system security
- ❌ CPU-level security features
- ❌ Primary antivirus software
- ❌ Firewall and network security

### Backup Layer When Primary Defenses Fail
QuantumShield **activates when primary defenses are compromised**:
- ✅ Device OS fails → We detect file tampering
- ✅ CPU security bypassed → We monitor malicious processes
- ✅ Antivirus misses threats → We catch suspicious behavior
- ✅ Ransomware gets through → We create emergency backups

## Technology Stack

- **Quantum Computing**: Qiskit 2.x, Qiskit Aer
- **Web Frameworks**: Streamlit 1.51+, Flask 3.x
- **Database**: SQLAlchemy (PostgreSQL/SQLite)
- **Visualization**: Matplotlib, Plotly
- **System Monitoring**: psutil
- **Scientific Computing**: NumPy

## Project Structure

```
QuantumShield/
├── main.py                  # Main entry point
├── app.py                   # Streamlit application
├── flask_app.py             # Flask application
├── database.py              # Database models and connections
├── file_monitor.py          # File integrity monitoring
├── malware_detector.py      # Malware detection engine
├── ransomware_detector.py   # Ransomware protection
├── templates/               # Flask HTML templates
└── pyproject.toml           # Project dependencies
```

## Documentation

- [Flask App Details](FLASK_README.md) - Flask-specific documentation
- [Replit Configuration](replit.md) - Replit deployment guide

## How It Works

1. **Quantum Matrix Creation**: Uses H(0) → CNOT(0,1) to create entangled Bell state
2. **Perfect Correlation**: Bell state ensures measurements are always 00 or 11
3. **Entropy-Based Storage**: Measurements secured with Shannon entropy keys
4. **Data Persistence**: Even when quantum state collapses, data is preserved
5. **Attack Detection**: Eavesdropping introduces decoherence, breaking Bell correlation
6. **Auto-Reset**: System detects correlation drop and automatically restores quantum state
7. **File Monitoring**: Real file integrity checking with quantum-secured checksums

## License

See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with Quantum Computing Principles** 🔬⚛️🔐

# 🔐 QuantumShield

**Quantum Entanglement Self-Healing Security System**

A multi-layered security monitoring system that combines quantum computing principles, file integrity monitoring, process analysis, and automated threat response. QuantumShield provides both a web-based dashboard and a REST API for comprehensive security monitoring.

## 🌟 Features

### Core Security Features
- 🔒 **Quantum-Based Detection**: Uses Bell state entanglement principles for tamper detection
- 📁 **File Integrity Monitoring**: Real-time monitoring of critical files with entropy analysis
- 🔍 **Process Monitoring**: Detects suspicious processes and malware behavior
- 🛡️ **Ransomware Protection**: Automated backup and recovery mechanisms
- 🤖 **Automated Response**: Self-healing capabilities with automated threat mitigation
- 📊 **Real-Time Analytics**: Live statistics and threat visualization

### Technology Stack
- **Quantum Computing**: Qiskit for quantum circuit simulation, QuTiP for quantum gate operations
- **Backend**: Flask REST API + Streamlit Dashboard
- **Database**: SQLAlchemy with PostgreSQL/SQLite support
- **Monitoring**: psutil for system resource tracking
- **Visualization**: Plotly, Matplotlib, Streamlit charts, Pygame for interactive quantum visualizations

## 📋 System Requirements

- Python 3.11 or higher
- SQLite (included) or PostgreSQL (recommended for production)
- Linux, macOS, or Windows
- 4GB RAM minimum
- Network access for dashboard

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/stephenvegagarcia/QuantumShield.git
cd QuantumShield

# Install dependencies
pip install -e .
```

### 2. Database Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and set your DATABASE_URL
# For development (SQLite):
DATABASE_URL=sqlite:///./quantumshield.db

# For production (PostgreSQL):
# DATABASE_URL=postgresql://user:password@localhost:5432/quantumshield
```

### 3. Start Services

**Option A: Start Both Services Automatically**
```bash
./start_services.sh
```

**Option B: Start Individually**

Terminal 1 - Flask API:
```bash
export DATABASE_URL=sqlite:///./quantumshield.db
python flask_app.py
```

Terminal 2 - Streamlit Dashboard:
```bash
export DATABASE_URL=sqlite:///./quantumshield.db
streamlit run app.py
```

### 4. Access the System

- **Flask API**: http://localhost:5000
- **Flask Dashboard**: http://localhost:5000/
- **Streamlit UI**: http://localhost:8501
- **API Health Check**: http://localhost:5000/api/health

### 5. Quantum Gate Visualizer (Interactive Demo)

Experience quantum gates in action with our interactive visualizer:

```bash
python quantum_gate_visualizer.py
```

**Features:**
- 🎮 **Interactive Controls**: Toggle shield, simulate attacks, switch between gate modes
- 🌈 **4D Tesseract Visualization**: See quantum states in a rotating hypercube
- ⚛️ **Multiple Gate Modes**: BELL, HXXH, CNOT, CZ, PAULI, PHASE
- 📊 **Real-time Entropy Display**: Monitor quantum entanglement and decoherence
- 🎨 **Color-coded Gates**: Each gate type has a unique visual signature

**Controls:**
- `[S]` - Toggle quantum shield (activate/deactivate)
- `[A]` - Toggle attack simulation (add noise)
- `[1-6]` - Switch between different quantum gate modes
  - `[1]` - BELL state (entangled qubits)
  - `[2]` - HXXH (Hadamard superposition)
  - `[3]` - CNOT (Controlled-NOT)
  - `[4]` - CZ (Controlled-Z phase)
  - `[5]` - PAULI (X, Y, Z randomization)
  - `[6]` - PHASE (S and P gates)

**What it demonstrates:**
- How quantum gates protect information through entanglement
- Visual representation of quantum state decoherence under attack
- Real-time entropy calculations showing quantum correlation
- 4D projection of quantum states in a tesseract

## 📚 Documentation

### Project Structure

```
QuantumShield/
├── flask_app.py                 # Flask REST API server
├── app.py                       # Streamlit dashboard
├── quantum_gate_visualizer.py   # Interactive quantum gate visualization
├── quantum_demo.py              # Quantum physics demonstration
├── database.py                  # Database models and setup
├── file_monitor.py              # File integrity monitoring
├── malware_detector.py          # Process and malware detection
├── ransomware_detector.py       # Ransomware protection
├── main.py                      # Legacy main entry point
├── test_api.py                  # API testing suite
├── start_services.sh            # Service startup script
├── stop_services.sh             # Service shutdown script
├── pyproject.toml               # Python dependencies
├── .env.example                 # Environment template
├── README_FLASK.md              # Flask API documentation
└── README.md                    # This file
```

### Database Schema

**Tables:**
- `security_events` - Security incidents and alerts
- `monitored_files` - Files under protection
- `quantum_measurements` - Quantum state measurements
- `system_state` - Overall system status
- `process_events` - Process monitoring data
- `threat_signatures` - Known threat patterns
- `automated_responses` - System response actions

## 🔌 API Endpoints

### System
- `GET /api/health` - Health check
- `GET /api/stats` - System statistics

### Security Events
- `GET /api/events/recent?limit=10` - Recent events
- `POST /api/events` - Create event

### File Monitoring
- `GET /api/files/monitored` - All monitored files
- `GET /api/files/monitored/<id>` - Specific file

### Quantum Measurements
- `GET /api/quantum/measurements?limit=20` - Get measurements
- `POST /api/quantum/measurements` - Create measurement

### System State
- `GET /api/system/state` - Get system state
- `PUT /api/system/state` - Update state

### Process Monitoring
- `GET /api/processes/recent?limit=10` - Recent processes
- `GET /api/processes/suspicious` - Suspicious processes

### Threats
- `GET /api/threats/signatures` - Threat signatures
- `GET /api/responses/automated?limit=20` - Automated responses

## 📖 Usage Examples

### Testing the API

```bash
# Run complete test suite
python test_api.py

# Test individual endpoints
curl http://localhost:5000/api/stats
curl http://localhost:5000/api/events/recent?limit=5
```

### Creating Security Events

```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "file_tampering",
    "reason": "Unauthorized modification detected",
    "entropy": 0.85,
    "correlation": 0.92
  }'
```

### Monitoring Files

```python
from file_monitor import add_monitored_file, scan_all_monitored_files

# Add a file to monitoring
add_monitored_file("/path/to/important/file.txt")

# Scan all monitored files
results = scan_all_monitored_files()
for result in results:
    print(f"File: {result['file_path']}, Status: {result['status']}")
```

### Process Monitoring

```python
from malware_detector import scan_running_processes

# Scan for suspicious processes
threats = scan_running_processes()
for threat in threats:
    print(f"Suspicious: {threat['name']} (Score: {threat['threat_score']})")
```

## 🛠️ Development

### Running in Debug Mode

```bash
# Flask with debug
export FLASK_DEBUG=True
python flask_app.py

# Streamlit with auto-reload (default)
streamlit run app.py
```

### Running Tests

```bash
# API tests
python test_api.py

# Check logs
tail -f flask.log
tail -f streamlit.log
```

### Database Migrations

```bash
# Initialize database
python -c "from database import init_db; init_db()"

# Reset database (caution!)
rm quantumshield.db
python -c "from database import init_db; init_db()"
```

## 🚢 Production Deployment

### Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Run with multiple workers
export DATABASE_URL=postgresql://user:pass@localhost/quantumshield
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -e .

ENV DATABASE_URL=sqlite:///./quantumshield.db

EXPOSE 5000 8501

CMD ["./start_services.sh"]
```

### Environment Variables

```bash
DATABASE_URL=postgresql://user:password@host:5432/db  # Required
PORT=5000                                              # Optional (default: 5000)
FLASK_ENV=production                                   # Optional
FLASK_DEBUG=False                                      # Optional
```

## 🔒 Security Considerations

### Defense-in-Depth Principle

QuantumShield is designed as a **secondary security layer**. It does NOT replace:
- ❌ Device OS security (iOS/Android)
- ❌ CPU security features (Intel SGX, ARM TrustZone)
- ❌ Primary antivirus software
- ❌ Firewall and network protection

### When QuantumShield Activates

This system provides backup protection when primary defenses fail:
- ✅ **Device OS compromised** → We detect file tampering
- ✅ **CPU security bypassed** → We monitor malicious processes
- ✅ **Antivirus misses threat** → We catch suspicious behavior
- ✅ **Ransomware breakthrough** → We create emergency backups

### Best Practices

1. **Database**: Use PostgreSQL for production (SQLite for dev only)
2. **HTTPS**: Always use SSL/TLS in production
3. **Authentication**: Add API authentication for public deployments
4. **Backups**: Regular database backups for security events
5. **Monitoring**: Set up alerting for critical security events
6. **Updates**: Keep dependencies updated for security patches

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check DATABASE_URL is set
echo $DATABASE_URL

# Test database connection
python -c "from database import get_db; db = get_db(); print('Connected!')"
```

### Port Already in Use

```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Flask Not Starting

```bash
# Check logs
cat flask.log

# Verify dependencies
pip install flask flask-cors sqlalchemy
```

### Streamlit Connection Error

```bash
# Check logs
cat streamlit.log

# Clear Streamlit cache
streamlit cache clear
```

## 📊 Monitoring & Analytics

### Key Metrics to Track

- **Security Events**: Total incidents over time
- **File Integrity**: Number of files protected and attacks prevented
- **Process Activity**: Suspicious processes detected
- **Quantum Measurements**: Correlation scores and entropy levels
- **Response Time**: Automated response effectiveness

### Dashboard Features

**Streamlit Dashboard**:
- Quantum circuit visualization
- Real-time Bell state measurements
- File monitoring status
- Process threat analysis
- Automated response logs

**Flask Dashboard**:
- Live statistics
- Recent security events table
- Monitored files status
- Process events timeline

## 📝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Qiskit**: IBM Quantum computing framework
- **Flask**: Web framework
- **Streamlit**: Dashboard framework
- **SQLAlchemy**: Database ORM

## 📧 Contact

For questions or support:
- GitHub: [@stephenvegagarcia](https://github.com/stephenvegagarcia)
- Repository: [QuantumShield](https://github.com/stephenvegagarcia/QuantumShield)

---

**⚠️ Important**: QuantumShield is designed as a backup security layer. Always maintain primary security measures including antivirus, firewall, and OS security updates.

**🔐 Stay Secure!**

# QuantumShield - Flask Application

This Flask application provides the same quantum security system functionality as the Streamlit app, but with a traditional web interface.

## Screenshots

### Main Dashboard
![Flask Dashboard](https://github.com/user-attachments/assets/6c531c70-476a-4587-9719-d32165dd94d2)

### File Integrity Monitor
![File Monitor](https://github.com/user-attachments/assets/fc0da8af-1ff2-41d5-acf8-9a32d4acb66e)

### Threat Detection
![Threat Detection](https://github.com/user-attachments/assets/277a9a20-7d4d-4597-80f5-69b7d2b55316)

## Features

The Flask app includes all the same features as the Streamlit version:

- **Quantum Entanglement Security System**: Bell State quantum circuit implementation
- **Attack Simulation**: Test the system's self-healing capabilities
- **File Integrity Monitoring**: Track and protect important files
- **Malware Detection**: Scan running processes for suspicious activity
- **Ransomware Protection**: Detect and prevent ransomware attacks
- **Automated Response**: Automatic threat mitigation
- **Data Persistence**: Quantum measurements stored with entropy keys

## Running the Flask App

### Prerequisites

1. **Database Configuration** (Optional):
   - Set the `DATABASE_URL` environment variable to your PostgreSQL connection string:
     ```bash
     export DATABASE_URL="postgresql://user:password@host:port/database"
     ```
   - If not set, the app will automatically use SQLite (`quantum_security.db`) as a fallback for testing

2. **Install dependencies**:
   ```bash
   pip install flask numpy qiskit qiskit-aer matplotlib psutil sqlalchemy pylatexenc
   ```
   
   Or install all dependencies from pyproject.toml:
   ```bash
   pip install -e .
   ```

### Start the Server

Run the Flask application:

```bash
python flask_app.py
```

The server will start on `http://0.0.0.0:5000`

Access it in your browser at:
- `http://localhost:5000` - Main Dashboard
- `http://localhost:5000/file-monitor` - File Integrity Monitor
- `http://localhost:5000/threat-detection` - Threat Detection

## Running the Streamlit App (Original)

If you prefer the original Streamlit interface:

```bash
streamlit run app.py
```

## API Endpoints

The Flask app provides the following API endpoints:

### Pages
- `GET /` - Main dashboard with quantum circuit visualization
- `GET /file-monitor` - File monitoring page
- `GET /threat-detection` - Threat detection page

### Quantum Operations
- `GET /measure` - Perform quantum measurement (returns JSON)
- `POST /attack` - Simulate attack on quantum system
- `POST /reset` - Reset system after attack
- `POST /upgrade` - Upgrade system version

### File Monitoring
- `POST /add-file` - Add file to monitor
- `POST /scan-files` - Scan all monitored files for tampering
- `POST /remove-file/<id>` - Remove file from monitoring

### Threat Detection
- `POST /scan-malware` - Scan running processes for malware
- `POST /scan-ransomware` - Scan for ransomware activity
- `POST /terminate-process/<pid>` - Terminate suspicious process

## Architecture

Both apps share the same backend code:
- `database.py` - Database models and connections (supports PostgreSQL and SQLite)
- `file_monitor.py` - File integrity monitoring with entropy-based checksums
- `malware_detector.py` - Process scanning and malware detection
- `ransomware_detector.py` - Ransomware detection and protection

### Flask App Components:
- `flask_app.py` - Flask routes and API endpoints
- `templates/base.html` - Base template with navigation and styling
- `templates/index.html` - Main dashboard with quantum circuit
- `templates/file_monitor.html` - File monitoring interface
- `templates/threat_detection.html` - Threat detection interface

### Streamlit App Components:
- `app.py` - Streamlit interface

## Development

Both applications can run simultaneously on different ports:
- Streamlit: Default port 8501
- Flask: Default port 5000

Choose the interface that best suits your needs!

## Technology Stack

- **Backend Framework**: Flask 3.x
- **Quantum Computing**: Qiskit 2.x, Qiskit Aer
- **Database**: SQLAlchemy (PostgreSQL/SQLite)
- **Frontend**: Bootstrap 5, jQuery
- **Visualization**: Matplotlib
- **System Monitoring**: psutil

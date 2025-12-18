# QuantumShield - Flask Application

This Flask application provides the same quantum security system functionality as the Streamlit app, but with a traditional web interface.

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

1. Set the `DATABASE_URL` environment variable to your PostgreSQL connection string:
   ```bash
   export DATABASE_URL="postgresql://user:password@host:port/database"
   ```

2. Install dependencies:
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

- `GET /` - Main dashboard
- `GET /measure` - Perform quantum measurement
- `POST /attack` - Simulate attack
- `POST /reset` - Reset system
- `POST /upgrade` - Upgrade system version
- `GET /file-monitor` - File monitoring page
- `POST /add-file` - Add file to monitor
- `POST /scan-files` - Scan monitored files
- `POST /remove-file/<id>` - Remove file from monitoring
- `GET /threat-detection` - Threat detection page
- `POST /scan-malware` - Scan for malware
- `POST /scan-ransomware` - Scan for ransomware
- `POST /terminate-process/<pid>` - Terminate suspicious process

## Architecture

Both apps share the same backend code:
- `database.py` - Database models and connections
- `file_monitor.py` - File integrity monitoring
- `malware_detector.py` - Process scanning and malware detection
- `ransomware_detector.py` - Ransomware detection and protection

The Flask app uses:
- `flask_app.py` - Flask routes and API
- `templates/` - HTML templates with Bootstrap UI

The Streamlit app uses:
- `app.py` - Streamlit interface

## Development

Both applications can run simultaneously on different ports:
- Streamlit: Default port 8501
- Flask: Default port 5000

Choose the interface that best suits your needs!

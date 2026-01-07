# QuantumShield Flask API

A Flask-based REST API for the QuantumShield security monitoring system.

## Features

- 🔒 Security event tracking and monitoring
- 📁 File monitoring and integrity checking
- 🔍 Process monitoring and threat detection
- ⚛️ Quantum measurement tracking
- 🤖 Automated response logging
- 📊 Real-time dashboard with statistics

## Setup

### 1. Install Dependencies

```bash
pip install flask flask-cors sqlalchemy psycopg2-binary
```

Or use the project dependencies:

```bash
pip install -e .
```

### 2. Configure Database

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and set your database URL:

**For SQLite (Development):**
```
DATABASE_URL=sqlite:///./quantumshield.db
```

**For PostgreSQL (Production):**
```
DATABASE_URL=postgresql://username:password@localhost:5432/quantumshield
```

### 3. Initialize Database

The database tables will be created automatically when you first run the Flask app.

### 4. Run the Flask App

```bash
python flask_app.py
```

Or with environment variables:

```bash
export DATABASE_URL=sqlite:///./quantumshield.db
python flask_app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Dashboard
- `GET /` - Web dashboard with real-time statistics

### System Stats
- `GET /api/stats` - Get overall system statistics
- `GET /api/health` - Health check endpoint
- `GET /api/deploy/readiness` - Deployment readiness recommendation

### Security Events
- `GET /api/events/recent?limit=10` - Get recent security events
- `POST /api/events` - Create a new security event

### File Monitoring
- `GET /api/files/monitored` - Get all monitored files
- `GET /api/files/monitored/<id>` - Get specific monitored file

### Quantum Measurements
- `GET /api/quantum/measurements?limit=20` - Get quantum measurements
- `POST /api/quantum/measurements` - Create a new quantum measurement

### System State
- `GET /api/system/state` - Get current system state
- `PUT /api/system/state` - Update system state

### Process Monitoring
- `GET /api/processes/recent?limit=10` - Get recent process events
- `GET /api/processes/suspicious` - Get suspicious processes

### Threat Intelligence
- `GET /api/threats/signatures` - Get all threat signatures

### Automated Responses
- `GET /api/responses/automated?limit=20` - Get automated responses

## Example API Usage

### Get System Stats
```bash
curl http://localhost:5000/api/stats
```

### Create Security Event
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "file_tampering",
    "reason": "Unauthorized file modification detected",
    "entropy": 0.85,
    "correlation": 0.92
  }'
```

### Get Recent Security Events
```bash
curl http://localhost:5000/api/events/recent?limit=5
```

### Create Quantum Measurement
```bash
curl -X POST http://localhost:5000/api/quantum/measurements \
  -H "Content-Type: application/json" \
  -d '{
    "entropy_key": 0.7854,
    "data_hash": 12345678,
    "correlation": 0.88,
    "measurements": {"00": 0.5, "11": 0.5},
    "is_attack": false
  }'
```

## Dashboard

Access the web dashboard at `http://localhost:5000/` to view:
- Real-time security statistics
- Recent security events
- Monitored files status
- Process events and threats
- Auto-refreshing every 5 seconds

## Database Schema

The Flask app uses the following tables:
- `security_events` - Security incidents and alerts
- `monitored_files` - Files being protected
- `quantum_measurements` - Quantum state measurements
- `system_state` - Overall system status
- `process_events` - Process monitoring data
- `threat_signatures` - Known threat patterns
- `automated_responses` - System response actions

## Development

### Running in Debug Mode
```bash
export FLASK_DEBUG=True
python flask_app.py
```

### Using Different Port
```bash
export PORT=8000
python flask_app.py
```

## Production Deployment

For production, use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
```

## Integration with Streamlit App

The Flask API runs independently from the Streamlit app (`app.py`). You can run both simultaneously:

**Terminal 1 - Flask API:**
```bash
python flask_app.py
```

**Terminal 2 - Streamlit Dashboard:**
```bash
streamlit run app.py
```

This gives you both:
- Streamlit UI for interactive quantum security monitoring
- Flask REST API for programmatic access and integrations

# QuantumShield - Quick Reference Guide

## 🚀 Quick Start Commands

### Start Everything
```bash
./start_services.sh
```

### Stop Everything
```bash
./stop_services.sh
```

### Start Individually
```bash
# Flask API
export DATABASE_URL=sqlite:///./quantumshield.db
python flask_app.py

# Streamlit Dashboard
streamlit run app.py
```

## 🔗 Access URLs

| Service | URL | Description |
|---------|-----|-------------|
| Flask API | http://localhost:5000 | REST API endpoints |
| Flask Dashboard | http://localhost:5000/ | Web-based monitoring |
| Streamlit UI | http://localhost:8501 | Interactive quantum dashboard |
| Health Check | http://localhost:5000/api/health | API status |

## 📊 Database Management

```bash
# Check database status
python setup_database.py status

# Initialize database
python setup_database.py init

# Add sample data
python setup_database.py sample

# Reset database (caution!)
python setup_database.py reset
```

## 🧪 Testing

```bash
# Run API tests
python test_api.py

# Test single endpoint
curl http://localhost:5000/api/stats

# Create test event
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{"event_type":"test","reason":"Testing"}'
```

## 📝 Common API Calls

### Get System Stats
```bash
curl http://localhost:5000/api/stats | jq
```

### Get Recent Security Events
```bash
curl http://localhost:5000/api/events/recent?limit=5 | jq
```

### Get Monitored Files
```bash
curl http://localhost:5000/api/files/monitored | jq
```

### Get Quantum Measurements
```bash
curl http://localhost:5000/api/quantum/measurements?limit=10 | jq
```

### Get System State
```bash
curl http://localhost:5000/api/system/state | jq
```

### Create Security Event
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "file_tampering",
    "reason": "Unauthorized modification",
    "entropy": 0.85,
    "correlation": 0.92
  }' | jq
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
  }' | jq
```

## 🔍 Monitoring & Logs

```bash
# View Flask logs
tail -f flask.log

# View Streamlit logs
tail -f streamlit.log

# Check running processes
ps aux | grep -E "flask_app|streamlit"

# Check ports
lsof -i :5000  # Flask
lsof -i :8501  # Streamlit
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill process
lsof -i :5000
kill -9 <PID>
```

### Database Issues
```bash
# Check connection
python -c "from database import get_db; get_db()"

# Reset database
python setup_database.py reset
```

### Service Won't Start
```bash
# Check logs
cat flask.log
cat streamlit.log

# Verify dependencies
pip install flask flask-cors sqlalchemy streamlit
```

## 🔧 Configuration

### Environment Variables
```bash
# Set database (in .env or export)
export DATABASE_URL=sqlite:///./quantumshield.db

# Or PostgreSQL
export DATABASE_URL=postgresql://user:pass@localhost/db

# Set Flask port
export PORT=5000

# Enable debug mode
export FLASK_DEBUG=True
```

### Database URLs

**SQLite (Development):**
```
DATABASE_URL=sqlite:///./quantumshield.db
```

**PostgreSQL (Production):**
```
DATABASE_URL=postgresql://username:password@localhost:5432/quantumshield
```

## 📦 Installation

```bash
# Install all dependencies
pip install -e .

# Install specific packages
pip install flask flask-cors sqlalchemy streamlit qiskit

# Install for production
pip install gunicorn
```

## 🚀 Production Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
```

### Using Docker
```bash
docker build -t quantumshield .
docker run -p 5000:5000 -p 8501:8501 quantumshield
```

## 📚 File Structure

```
QuantumShield/
├── flask_app.py           # Flask REST API ⭐
├── app.py                 # Streamlit UI ⭐
├── database.py            # Database models ⭐
├── file_monitor.py        # File monitoring
├── malware_detector.py    # Process detection
├── ransomware_detector.py # Ransomware protection
├── test_api.py           # API tests
├── setup_database.py     # DB management ⭐
├── start_services.sh     # Start script ⭐
├── stop_services.sh      # Stop script ⭐
├── .env.example          # Config template
└── README.md             # Documentation

⭐ = Most frequently used
```

## 💡 Pro Tips

1. **Always check database status before starting:**
   ```bash
   python setup_database.py status
   ```

2. **Use environment variables for configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Monitor logs in real-time:**
   ```bash
   tail -f flask.log streamlit.log
   ```

4. **Use jq for pretty JSON output:**
   ```bash
   curl http://localhost:5000/api/stats | jq
   ```

5. **Test API before integrating:**
   ```bash
   python test_api.py
   ```

## 🆘 Support

- **Documentation**: README.md, README_FLASK.md
- **API Tests**: `python test_api.py`
- **Database Help**: `python setup_database.py help`
- **Logs**: Check flask.log and streamlit.log
- **GitHub**: https://github.com/stephenvegagarcia/QuantumShield

## ⚡ Keyboard Shortcuts

### Streamlit
- `R` - Rerun the app
- `C` - Clear cache
- `?` - Show keyboard shortcuts

### Terminal
- `Ctrl+C` - Stop service
- `Ctrl+Z` - Suspend (use `fg` to resume)

---

**Last Updated**: December 2025  
**Version**: 1.0.0

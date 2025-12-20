#!/bin/bash
# QuantumShield Startup Script
# Start both Flask API and Streamlit dashboard

echo "🔐 Starting QuantumShield Security System..."

# Set database URL
export DATABASE_URL=sqlite:///./quantumshield.db

# Start Flask API
echo "📡 Starting Flask API with Web Dashboard on port 5000..."
nohup python flask_app.py > flask.log 2>&1 &
FLASK_PID=$!
echo "   Flask API started (PID: $FLASK_PID)"

# Wait for Flask to start
sleep 3

echo ""
echo "✅ QuantumShield is running!"
echo ""
echo "📊 Access points:"
echo "   - Flask API:          http://localhost:5000/api/health"
echo "   - Web Dashboard:      http://localhost:5000/"
echo "   - Security Info:      http://localhost:5000/api/security/info"
echo ""
echo "📝 Logs:"
echo "   - Flask:     tail -f flask.log"
echo ""
echo "🛑 To stop service:"
echo "   kill $FLASK_PID"
echo "   or run: ./stop_services.sh"
echo ""

# Save PID for later
echo $FLASK_PID > .flask.pid

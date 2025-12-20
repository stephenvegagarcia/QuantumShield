#!/bin/bash
# Stop QuantumShield services

echo "🛑 Stopping QuantumShield services..."

if [ -f .flask.pid ]; then
    FLASK_PID=$(cat .flask.pid)
    if kill -0 $FLASK_PID 2>/dev/null; then
        kill $FLASK_PID
        echo "   ✓ Stopped Flask API (PID: $FLASK_PID)"
    fi
    rm .flask.pid
fi

# Cleanup any remaining processes
pkill -f "python flask_app.py" 2>/dev/null

echo ""
echo "✅ All services stopped"

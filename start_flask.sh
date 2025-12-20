#!/bin/bash
# Start Flask app with proper environment configuration

# Set database URL if not already set
export DATABASE_URL="${DATABASE_URL:-sqlite:///./quantumshield.db}"

# Initialize database if needed
echo "Initializing database..."
python setup_database.py initialize

# Start Flask app
echo "Starting Flask app on port 5000..."
python flask_app.py

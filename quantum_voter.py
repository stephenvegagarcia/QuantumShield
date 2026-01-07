"""
Quantum Voter AI - Security Gatekeeper and Builder Assistant

This module implements an AI-based idea submission system with:
- Security fingerprinting using SHA-256 hashes
- AI voting/advice system for categorizing ideas
- JSON-based database for storing ideas with proofs
- Web interface for idea submission and viewing
"""

import hashlib
import json
import os
import time
from typing import Dict, List, Any
from flask import Blueprint, request, jsonify, render_template_string

# Create Blueprint for quantum voter
quantum_voter_bp = Blueprint('quantum_voter', __name__)

DB_FILE = 'quantum_voter_network.json'


def get_ai_advice(idea_text: str) -> str:
    """
    Acts as the security gatekeeper and builder-assistant.
    This function uses a logic-based filter to categorize and provide
    advice on submitted ideas.
    
    Args:
        idea_text: The idea text to analyze
        
    Returns:
        AI-generated advice or error message
    """
    # Validate entropy
    if len(idea_text) < 5:
        return "ERROR: Entropy too low. Please expand your thought."
    
    # AI Logic: Categorizing the idea
    categories = {
        "app": "Architecture: Modular Flask backend suggested.",
        "art": "Visual: Consider using Canvas API for the UI.",
        "hardware": "Physical: Raspberry Pi or ESP32 integration possible.",
        "web": "Network: Suggesting JSON-based API structure.",
        "security": "Security: Quantum-based encryption recommended.",
        "quantum": "Quantum: Consider Qiskit integration for quantum circuits.",
        "blockchain": "Blockchain: Distributed ledger for immutable proofs suggested.",
        "ai": "AI: Machine learning model integration possible.",
        "database": "Database: SQLAlchemy ORM with PostgreSQL recommended.",
        "api": "API: RESTful design with proper authentication suggested."
    }
    
    advice = "BUILDER NOTE: High-level potential detected. Secure your proof."
    for key in categories:
        if key in idea_text.lower():
            advice = f"AI SUGGESTION: {categories[key]}"
            break
            
    return advice


def init_voter_db() -> None:
    """Initialize the quantum voter database if it doesn't exist"""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump([], f)


def save_idea(content: str, fingerprint: str, ai_note: str) -> None:
    """
    Save an idea to the quantum voter network database using atomic writes
    
    Args:
        content: The idea text content
        fingerprint: SHA-256 hash of the content
        ai_note: AI-generated advice for the idea
    """
    import tempfile
    import shutil
    
    # Read current data
    with open(DB_FILE, 'r') as f:
        data = json.load(f)
    
    # Add new idea
    data.append({
        "timestamp": time.ctime(),
        "idea": content,
        "hash": fingerprint,
        "ai_note": ai_note
    })
    
    # Write to temporary file first (atomic operation)
    temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(DB_FILE), text=True)
    try:
        with os.fdopen(temp_fd, 'w') as f:
            json.dump(data, f, indent=4)
        # Atomically replace the original file
        shutil.move(temp_path, DB_FILE)
    except Exception:
        # Clean up temp file on error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise


def get_all_ideas() -> List[Dict[str, Any]]:
    """
    Retrieve all ideas from the database
    
    Returns:
        List of idea dictionaries
    """
    if not os.path.exists(DB_FILE):
        init_voter_db()
    
    with open(DB_FILE, 'r') as f:
        return json.load(f)


# HTML UI Template
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Voter - AI Security Gatekeeper</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
            padding: 40px;
        }
        
        h1 {
            color: #1e3c72;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-style: italic;
        }
        
        .input-section {
            margin-bottom: 30px;
        }
        
        label {
            display: block;
            color: #333;
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #7e22ce;
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(118, 75, 162, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .result {
            margin-top: 20px;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }
        
        .result.success {
            background: #d4edda;
            border: 2px solid #28a745;
            color: #155724;
        }
        
        .result.error {
            background: #f8d7da;
            border: 2px solid #dc3545;
            color: #721c24;
        }
        
        .hash-display {
            word-break: break-all;
            font-family: 'Courier New', monospace;
            background: rgba(0, 0, 0, 0.05);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .ai-note {
            font-weight: bold;
            color: #7e22ce;
            margin-top: 10px;
        }
        
        .logs-section {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #ddd;
        }
        
        .log-entry {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 10px;
            border-left: 4px solid #7e22ce;
        }
        
        .log-timestamp {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        
        .log-idea {
            color: #333;
            margin: 10px 0;
        }
        
        .log-hash {
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            color: #666;
            word-break: break-all;
        }
        
        .log-ai {
            color: #7e22ce;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .toggle-logs {
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔮 Quantum Voter</h1>
        <p class="subtitle">AI Security Gatekeeper & Builder Assistant</p>
        
        <div class="input-section">
            <label for="ideaInput">Submit Your Idea:</label>
            <textarea 
                id="ideaInput" 
                rows="6" 
                placeholder="Enter your idea here... The AI will analyze and provide architectural advice."
            ></textarea>
        </div>
        
        <button onclick="submitIdea()">🚀 Submit & Get AI Advice</button>
        
        <div id="result" class="result"></div>
        
        <div class="logs-section">
            <button class="toggle-logs" onclick="toggleLogs()">📋 View All Submissions</button>
            <div id="logs" style="display: none;"></div>
        </div>
    </div>
    
    <script>
        async function submitIdea() {
            const ideaText = document.getElementById('ideaInput').value;
            const resultDiv = document.getElementById('result');
            
            if (!ideaText.trim()) {
                resultDiv.className = 'result error';
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '⚠️ Please enter an idea before submitting.';
                return;
            }
            
            try {
                const response = await fetch('/quantum-voter/api/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ idea: ideaText })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    resultDiv.className = 'result success';
                    resultDiv.innerHTML = `
                        <strong>✅ Idea Submitted Successfully!</strong>
                        <div class="hash-display">
                            <strong>Security Hash:</strong><br>
                            ${data.hash}
                        </div>
                        <div class="ai-note">
                            ${data.ai_note}
                        </div>
                    `;
                    document.getElementById('ideaInput').value = '';
                    
                    // Refresh logs if visible
                    const logsDiv = document.getElementById('logs');
                    if (logsDiv.style.display !== 'none') {
                        loadLogs();
                    }
                } else {
                    throw new Error(data.error || 'Submission failed');
                }
                
                resultDiv.style.display = 'block';
            } catch (error) {
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `⚠️ Error: ${error.message}`;
                resultDiv.style.display = 'block';
            }
        }
        
        async function loadLogs() {
            try {
                const response = await fetch('/quantum-voter/api/logs');
                const logs = await response.json();
                const logsDiv = document.getElementById('logs');
                
                if (logs.length === 0) {
                    logsDiv.innerHTML = '<p style="text-align: center; color: #666;">No submissions yet.</p>';
                    return;
                }
                
                logsDiv.innerHTML = logs.reverse().map(log => `
                    <div class="log-entry">
                        <div class="log-timestamp">⏰ ${log.timestamp}</div>
                        <div class="log-idea"><strong>Idea:</strong> ${log.idea}</div>
                        <div class="log-hash"><strong>Hash:</strong> ${log.hash}</div>
                        <div class="log-ai">🤖 ${log.ai_note}</div>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Failed to load logs:', error);
            }
        }
        
        function toggleLogs() {
            const logsDiv = document.getElementById('logs');
            if (logsDiv.style.display === 'none') {
                logsDiv.style.display = 'block';
                loadLogs();
            } else {
                logsDiv.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""


# Routes
@quantum_voter_bp.route('/')
def home():
    """Render the quantum voter UI"""
    return render_template_string(HTML_UI)


@quantum_voter_bp.route('/api/submit', methods=['POST'])
def submit():
    """
    Submit an idea for AI analysis and security fingerprinting
    
    Returns:
        JSON response with status, hash, and AI advice
    """
    try:
        data = request.get_json()
        if not data or 'idea' not in data:
            return jsonify({"error": "Missing 'idea' field"}), 400
        
        idea_text = data['idea']
        
        # 1. Generate Security Hash (Entropy)
        fingerprint = hashlib.sha256(idea_text.encode()).hexdigest()
        
        # 2. Get AI Advice (The Voter)
        ai_note = get_ai_advice(idea_text)
        
        # Check for error in AI advice
        if ai_note.startswith("ERROR:"):
            return jsonify({"error": ai_note}), 400
        
        # 3. Save to the JSON Network
        save_idea(idea_text, fingerprint, ai_note)
        
        return jsonify({
            "status": "success",
            "hash": fingerprint,
            "ai_note": ai_note
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@quantum_voter_bp.route('/api/logs')
def logs():
    """
    Retrieve all submitted ideas from the database
    
    Returns:
        JSON array of all ideas with their metadata
    """
    try:
        all_ideas = get_all_ideas()
        return jsonify(all_ideas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Initialize database on module import
init_voter_db()

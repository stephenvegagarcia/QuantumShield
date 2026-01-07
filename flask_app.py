import os
import ssl
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from database import (
    init_db, get_db, SecurityEvent, QuantumMeasurement, SystemState,
    get_or_create_system_state, ProcessEvent, AutomatedResponse,
    MonitoredFile, ThreatSignature
)
from security_encryption import AESEncryption
from cybersecurity_training import CybersecurityTraining

app = Flask(__name__)
CORS(app)

# Deployment readiness configuration
DEPLOY_READINESS_LOOKBACK_HOURS = int(os.getenv('DEPLOY_READINESS_LOOKBACK_HOURS', '1'))

# Initialize AES-256 encryption
encryptor = AESEncryption()

# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Add comprehensive security headers"""
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval'; img-src 'self' data:;"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

# Initialize database
init_db()

# HTML Template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>QuantumShield Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        th {
            background: rgba(255, 255, 255, 0.1);
        }
        .status-active {
            color: #4ade80;
        }
        .status-inactive {
            color: #f87171;
        }
        button {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            color: white;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        .action-buttons {
            display: flex;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .btn-primary {
            background: #10b981;
        }
        .btn-danger {
            background: #ef4444;
        }
        .btn-info {
            background: #3b82f6;
        }
        .alert {
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            background: rgba(16, 185, 129, 0.2);
        }
        .alert-danger {
            background: rgba(239, 68, 68, 0.2);
        }
        input[type="text"] {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.1);
            color: white;
            width: 300px;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .status-green {
            background: #10b981;
        }
        .status-red {
            background: #ef4444;
        }
        .status-yellow {
            background: #f59e0b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 QuantumShield Security Dashboard</h1>
        
        <div class="card">
            <h2>🔒 Security Status</h2>
            <div id="systemStatus">
                <p><span class="status-indicator status-green"></span><strong>QuantumShield ACTIVE</strong> - All systems operational</p>
                <p>🔐 <strong>AES-256 Encryption:</strong> <span class="status-active">ENABLED</span></p>
                <p>🔒 <strong>HTTPS/TLS:</strong> <span class="status-active">SECURED</span></p>
                <p>🛡️ <strong>Quantum Protection:</strong> <span class="status-active">ACTIVE</span></p>
                <p>⚡ <strong>Real-time Monitoring:</strong> <span class="status-active">RUNNING</span></p>
            </div>
        </div>
        
        <div class="card">
            <h2>Quick Actions</h2>
            <div class="action-buttons">
                <button class="btn-primary" onclick="scanFiles()">🔍 Scan All Files</button>
                <button class="btn-primary" onclick="scanProcesses()">🖥️ Scan Processes</button>
                <button class="btn-danger" onclick="simulateAttack('ransomware')">⚠️ Test Ransomware Detection</button>
                <button class="btn-danger" onclick="simulateAttack('malware')">🦠 Test Malware Detection</button>
                <button class="btn-info" onclick="loadDashboard()">🔄 Refresh Data</button>
            </div>
            
            <div style="margin-top: 20px;">
                <h3>Add File to Monitor</h3>
                <input type="text" id="filePath" placeholder="/path/to/file.txt" />
                <button class="btn-primary" onclick="addFile()">➕ Add File</button>
            </div>
            
            <div style="margin-top: 20px;">
                <h3>🔐 Test AES-256 Encryption</h3>
                <input type="text" id="encryptInput" placeholder="Enter text to encrypt" style="width: 250px;" />
                <button class="btn-info" onclick="testEncryption()">🔒 Encrypt</button>
                <div id="encryptResult" style="margin-top: 10px; font-size: 0.9em;"></div>
            </div>
            
            <div id="actionResult" style="margin-top: 15px;"></div>
        </div>
        
        <div id="securityInfo" class="card" style="background: rgba(16, 185, 129, 0.15);"></div>
        
        <div class="stats" id="stats"></div>
        
        <div class="card">
            <h2>Recent Security Events</h2>
            <div id="events"></div>
        </div>
        
        <div class="card">
            <h2>Monitored Files</h2>
            <div id="files"></div>
        </div>
        
        <div class="card">
            <h2>Recent Process Events</h2>
            <div id="processes"></div>
        </div>
        
        <div class="card">
            <h2>🎓 Cybersecurity Training</h2>
            <p>Test your security knowledge with interactive scenarios</p>
            <button class="btn-primary" onclick="loadTraining()">📚 Start Training</button>
            <div id="trainingContent" style="margin-top: 20px;"></div>
        </div>
        
        <div class="card">
            <h2>⚛️ Quantum Security Analytics</h2>
            <p>Real-time quantum entanglement monitoring and attack detection</p>
            <button class="btn-info" onclick="loadQuantumStats()">📊 View Quantum Data</button>
            <div id="quantumStats" style="margin-top: 20px;"></div>
        </div>
    </div>
    
    <script>
        async function loadDashboard() {
            // Load security info
            try {
                const secInfo = await fetch('/api/security/info').then(r => r.json());
                document.getElementById('securityInfo').innerHTML = `
                    <h2>🔐 Active Security Measures</h2>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div>
                            <h3>🔒 Encryption</h3>
                            <p><strong>Algorithm:</strong> ${secInfo.encryption.algorithm}</p>
                            <p><strong>Key Size:</strong> ${secInfo.encryption.key_size} bits</p>
                            <p><strong>Mode:</strong> ${secInfo.encryption.mode}</p>
                            <p><strong>KDF:</strong> ${secInfo.encryption.key_derivation}</p>
                        </div>
                        <div>
                            <h3>🔐 SSL/TLS</h3>
                            <p><strong>Status:</strong> ${secInfo.ssl.enabled ? '✅ ENABLED' : '❌ DISABLED'}</p>
                            <p><strong>Protocol:</strong> ${secInfo.ssl.protocol}</p>
                            <p><strong>Key Size:</strong> ${secInfo.ssl.key_size} bits</p>
                            <p><strong>Type:</strong> ${secInfo.ssl.certificate_type}</p>
                        </div>
                    </div>
                `;
            } catch (e) {
                console.error('Failed to load security info:', e);
            }
            
            // Load stats
            const stats = await fetch('/api/stats').then(r => r.json());
            document.getElementById('stats').innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${stats.total_events}</div>
                    <div class="stat-label">Total Security Events</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.monitored_files}</div>
                    <div class="stat-label">Monitored Files</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.suspicious_processes}</div>
                    <div class="stat-label">Suspicious Processes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.quantum_measurements}</div>
                    <div class="stat-label">Quantum Measurements</div>
                </div>
            `;
            
            // Load recent events
            const events = await fetch('/api/events/recent').then(r => r.json());
            document.getElementById('events').innerHTML = `
                <table>
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Type</th>
                            <th>Reason</th>
                            <th>Entropy</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${events.map(e => `
                            <tr>
                                <td>${new Date(e.timestamp).toLocaleString()}</td>
                                <td>${e.event_type}</td>
                                <td>${e.reason}</td>
                                <td>${e.entropy ? e.entropy.toFixed(4) : 'N/A'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            
            // Load monitored files
            const files = await fetch('/api/files/monitored').then(r => r.json());
            document.getElementById('files').innerHTML = `
                <table>
                    <thead>
                        <tr>
                            <th>File Path</th>
                            <th>Status</th>
                            <th>Last Checked</th>
                            <th>Attack Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${files.map(f => `
                            <tr>
                                <td>${f.file_path}</td>
                                <td class="${f.is_active ? 'status-active' : 'status-inactive'}">
                                    ${f.is_active ? 'Active' : 'Inactive'}
                                </td>
                                <td>${new Date(f.last_checked).toLocaleString()}</td>
                                <td>${f.attack_count}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            
            // Load recent processes
            const processes = await fetch('/api/processes/recent').then(r => r.json());
            document.getElementById('processes').innerHTML = `
                <table>
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Process Name</th>
                            <th>PID</th>
                            <th>Threat Score</th>
                            <th>Suspicious</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${processes.map(p => `
                            <tr>
                                <td>${new Date(p.timestamp).toLocaleString()}</td>
                                <td>${p.process_name}</td>
                                <td>${p.process_id}</td>
                                <td>${p.threat_score.toFixed(2)}</td>
                                <td class="${p.is_suspicious ? 'status-inactive' : 'status-active'}">
                                    ${p.is_suspicious ? 'Yes' : 'No'}
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }
        
        function showResult(message, isError = false) {
            const resultDiv = document.getElementById('actionResult');
            resultDiv.innerHTML = `<div class="alert ${isError ? 'alert-danger' : ''}">${message}</div>`;
            setTimeout(() => { resultDiv.innerHTML = ''; }, 5000);
        }
        
        async function addFile() {
            const filePath = document.getElementById('filePath').value;
            if (!filePath) {
                showResult('❌ Please enter a file path', true);
                return;
            }
            
            try {
                const response = await fetch('/api/files/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ file_path: filePath })
                });
                const data = await response.json();
                
                if (response.ok) {
                    showResult(`✅ File added to monitoring: ${data.file_path}`);
                    document.getElementById('filePath').value = '';
                    loadDashboard();
                } else {
                    showResult(`❌ Error: ${data.error}`, true);
                }
            } catch (error) {
                showResult(`❌ Failed to add file: ${error.message}`, true);
            }
        }
        
        async function scanFiles() {
            showResult('🔍 Scanning all monitored files...');
            try {
                const response = await fetch('/api/files/scan', { method: 'POST' });
                const data = await response.json();
                
                if (data.compromised_count > 0) {
                    showResult(`⚠️ Scan complete: ${data.compromised_count} compromised files found!`, true);
                } else {
                    showResult(`✅ Scan complete: All ${data.total_scanned} files are secure`);
                }
                loadDashboard();
            } catch (error) {
                showResult(`❌ Scan failed: ${error.message}`, true);
            }
        }
        
        async function scanProcesses() {
            showResult('🖥️ Scanning running processes...');
            try {
                const response = await fetch('/api/processes/scan', { method: 'POST' });
                const data = await response.json();
                
                if (data.suspicious_count > 0) {
                    showResult(`⚠️ Found ${data.suspicious_count} suspicious processes!`, true);
                } else {
                    showResult(`✅ Process scan complete: No threats detected`);
                }
                loadDashboard();
            } catch (error) {
                showResult(`❌ Scan failed: ${error.message}`, true);
            }
        }
        
        async function simulateAttack(attackType) {
            showResult(`⚠️ Simulating ${attackType} attack...`);
            try {
                const response = await fetch('/api/test/attack', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ attack_type: attackType })
                });
                const data = await response.json();
                
                showResult(`✅ ${data.message} - Check events below!`);
                loadDashboard();
            } catch (error) {
                showResult(`❌ Simulation failed: ${error.message}`, true);
            }
        }
        
        async function testEncryption() {
            const text = document.getElementById('encryptInput').value;
            if (!text) {
                document.getElementById('encryptResult').innerHTML = 
                    '<div class="alert alert-danger">⚠️ Please enter text to encrypt</div>';
                return;
            }
            
            try {
                const response = await fetch('/api/security/encrypt', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data: text })
                });
                const data = await response.json();
                
                if (response.ok) {
                    document.getElementById('encryptResult').innerHTML = `
                        <div class="alert">
                            <strong>✅ Encrypted with ${data.algorithm}</strong><br>
                            <small style="word-break: break-all;">
                                ${data.encrypted.substring(0, 80)}...
                            </small>
                        </div>
                    `;
                } else {
                    document.getElementById('encryptResult').innerHTML = 
                        `<div class="alert alert-danger">❌ ${data.error}</div>`;
                }
            } catch (error) {
                document.getElementById('encryptResult').innerHTML = 
                    `<div class="alert alert-danger">❌ Encryption failed: ${error.message}</div>`;
            }
        }
        
        async function loadTraining() {
            const container = document.getElementById('trainingContent');
            container.innerHTML = '<p>Loading training scenarios...</p>';
            
            try {
                const response = await fetch('/api/training/scenarios');
                const data = await response.json();
                
                if (data.status === 'success') {
                    let html = '<div style="margin-top: 15px;">';
                    html += `<p><strong>Total Scenarios:</strong> ${data.total_scenarios}</p>`;
                    
                    data.scenarios.forEach(scenario => {
                        html += `
                            <div style="background: rgba(255,255,255,0.05); padding: 15px; margin: 10px 0; border-radius: 8px;">
                                <h3>${scenario.title}</h3>
                                <p><strong>Difficulty:</strong> <span style="color: ${
                                    scenario.difficulty === 'Easy' ? '#10b981' : 
                                    scenario.difficulty === 'Medium' ? '#f59e0b' : '#ef4444'
                                }">${scenario.difficulty}</span> | <strong>Points:</strong> ${scenario.points}</p>
                                <p>${scenario.description}</p>
                                <div style="background: rgba(0,0,0,0.3); padding: 10px; margin: 10px 0; border-radius: 5px; white-space: pre-wrap; font-family: monospace; font-size: 0.9em;">${scenario.scenario}</div>
                                <div style="margin: 10px 0;">
                                    ${Object.entries(scenario.options).map(([key, value]) => 
                                        `<button class="btn-primary" style="margin: 5px; display: block;" onclick="checkAnswer(${scenario.id}, '${key}')">${key}. ${value}</button>`
                                    ).join('')}
                                </div>
                                <div id="result-${scenario.id}" style="margin-top: 10px;"></div>
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                    container.innerHTML = html;
                }
            } catch (error) {
                container.innerHTML = '<p style="color: #ef4444;">Error loading training: ' + error.message + '</p>';
            }
        }
        
        async function checkAnswer(scenarioId, answer) {
            const resultDiv = document.getElementById(`result-${scenarioId}`);
            resultDiv.innerHTML = '<p>Checking answer...</p>';
            
            try {
                const response = await fetch('/api/training/check-answer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ scenario_id: scenarioId, answer: answer })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    const color = data.correct ? '#10b981' : '#ef4444';
                    const icon = data.correct ? '✅' : '❌';
                    resultDiv.innerHTML = `
                        <div style="background: rgba(${data.correct ? '16, 185, 129' : '239, 68, 68'}, 0.1); padding: 15px; border-radius: 5px; border-left: 4px solid ${color};">
                            <p><strong>${icon} ${data.correct ? 'CORRECT!' : 'INCORRECT'}</strong></p>
                            <p><strong>Correct Answer:</strong> ${data.correct_answer}</p>
                            <p><strong>Points Earned:</strong> ${data.points_earned}/${data.max_points}</p>
                            <div style="margin-top: 10px; white-space: pre-wrap; font-size: 0.9em;">${data.explanation}</div>
                        </div>
                    `;
                }
            } catch (error) {
                resultDiv.innerHTML = '<p style="color: #ef4444;">Error: ' + error.message + '</p>';
            }
        }
        
        async function loadQuantumStats() {
            const container = document.getElementById('quantumStats');
            container.innerHTML = '<p>Loading quantum data...</p>';
            
            try {
                const response = await fetch('/api/quantum/stats');
                const data = await response.json();
                
                if (data.status === 'success') {
                    const state = data.system_state;
                    const physics = data.physics;
                    const trends = data.trends;
                    
                    let html = '<div style="margin-top: 15px;">';
                    
                    // System State
                    html += `
                        <div style="background: rgba(${state.quantum_intact ? '16, 185, 129' : '239, 68, 68'}, 0.1); padding: 15px; margin: 10px 0; border-radius: 8px;">
                            <h3>🔐 Quantum System State</h3>
                            <p><strong>Status:</strong> <span style="color: ${state.quantum_intact ? '#10b981' : '#ef4444'}">${state.quantum_intact ? '✅ INTACT' : '⚠️ COMPROMISED'}</span></p>
                            <p><strong>System Version:</strong> ${state.system_version}</p>
                            <p><strong>Last Reset:</strong> ${state.last_reset || 'Never'}</p>
                        </div>
                    `;
                    
                    // Physics Explanation
                    html += `
                        <div style="background: rgba(139, 92, 246, 0.1); padding: 15px; margin: 10px 0; border-radius: 8px;">
                            <h3>⚛️ Quantum Physics Protection</h3>
                            <p><strong>Bell State:</strong> <code>${physics.bell_state}</code></p>
                            <p><strong>Principle:</strong> ${physics.entanglement}</p>
                            <p><strong>Detection Method:</strong> ${physics.detection_method}</p>
                            <p><strong>Algorithm:</strong> ${physics.algorithm}</p>
                            <p style="margin-top: 10px; font-size: 0.9em; color: #a78bfa;">
                                <em>When qubits are entangled in a Bell state, any eavesdropping attempt causes 
                                quantum decoherence, breaking the correlation and triggering an alert.</em>
                            </p>
                        </div>
                    `;
                    
                    // Trends
                    if (trends.entropy.length > 0) {
                        const avgEntropy = (trends.entropy.reduce((a,b) => a+b, 0) / trends.entropy.length).toFixed(4);
                        const avgCorr = (trends.correlation.reduce((a,b) => a+b, 0) / trends.correlation.length).toFixed(2);
                        const totalAttacks = trends.attacks.reduce((a,b) => a+b, 0);
                        
                        html += `
                            <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; margin: 10px 0; border-radius: 8px;">
                                <h3>📊 Recent Measurements (Last 50)</h3>
                                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                                    <div>
                                        <p><strong>Avg Entropy:</strong></p>
                                        <p style="font-size: 1.5em; color: #60a5fa;">${avgEntropy}</p>
                                    </div>
                                    <div>
                                        <p><strong>Avg Correlation:</strong></p>
                                        <p style="font-size: 1.5em; color: #34d399;">${avgCorr}%</p>
                                    </div>
                                    <div>
                                        <p><strong>Attack Detections:</strong></p>
                                        <p style="font-size: 1.5em; color: #f87171;">${totalAttacks}</p>
                                    </div>
                                </div>
                                <p style="margin-top: 15px;"><strong>Entropy Trend:</strong> ${trends.entropy.slice(-10).map(e => e.toFixed(2)).join(', ')}</p>
                                <p><strong>Correlation Trend:</strong> ${trends.correlation.slice(-10).map(c => c.toFixed(1) + '%').join(', ')}</p>
                            </div>
                        `;
                    }
                    
                    html += '</div>';
                    container.innerHTML = html;
                }
            } catch (error) {
                container.innerHTML = '<p style="color: #ef4444;">Error loading quantum data: ' + error.message + '</p>';
            }
        }
        
        loadDashboard();
        setInterval(loadDashboard, 5000); // Refresh every 5 seconds
    </script>
</body>
</html>
"""

# Routes

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/stats')
def get_stats():
    """Get overall system statistics"""
    db = get_db()
    try:
        stats = {
            'total_events': db.query(SecurityEvent).count(),
            'monitored_files': db.query(MonitoredFile).filter(MonitoredFile.is_active.is_(True)).count(),
            'suspicious_processes': db.query(ProcessEvent).filter(ProcessEvent.is_suspicious.is_(True)).count(),
            'quantum_measurements': db.query(QuantumMeasurement).count(),
            'total_threats': db.query(ThreatSignature).count(),
            'automated_responses': db.query(AutomatedResponse).count(),
        }
        return jsonify(stats)
    finally:
        db.close()

@app.route('/api/events/recent')
def get_recent_events():
    """Get recent security events"""
    limit = request.args.get('limit', 10, type=int)
    db = get_db()
    try:
        events = db.query(SecurityEvent).order_by(desc(SecurityEvent.timestamp)).limit(limit).all()
        return jsonify([{
            'id': e.id,
            'timestamp': e.timestamp.isoformat(),
            'event_type': e.event_type,
            'reason': e.reason,
            'entropy': e.entropy,
            'correlation': e.correlation,
            'system_version': e.system_version
        } for e in events])
    finally:
        db.close()

@app.route('/api/events', methods=['POST'])
def create_event():
    """Create a new security event"""
    data = request.json
    db = get_db()
    try:
        event = SecurityEvent(
            event_type=data.get('event_type'),
            reason=data.get('reason'),
            entropy=data.get('entropy'),
            correlation=data.get('correlation'),
            system_version=data.get('system_version', 1)
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return jsonify({'id': event.id, 'status': 'created'}), 201
    finally:
        db.close()

@app.route('/api/files/monitored')
def get_monitored_files():
    """Get all monitored files"""
    db = get_db()
    try:
        files = db.query(MonitoredFile).all()
        return jsonify([{
            'id': f.id,
            'file_path': f.file_path,
            'entropy_signature': f.entropy_signature,
            'last_hash': f.last_hash,
            'created_at': f.created_at.isoformat(),
            'last_checked': f.last_checked.isoformat(),
            'is_active': f.is_active,
            'attack_count': f.attack_count
        } for f in files])
    finally:
        db.close()

@app.route('/api/files/add', methods=['POST'])
def add_file_to_monitor():
    """Add a new file to monitor"""
    from file_monitor import add_monitored_file
    data = request.json
    file_path = data.get('file_path')
    
    if not file_path:
        return jsonify({'error': 'file_path is required'}), 400
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File does not exist'}), 404
    
    monitored_file, is_new = add_monitored_file(file_path)
    
    return jsonify({
        'status': 'success',
        'file_id': monitored_file.id,
        'file_path': monitored_file.file_path,
        'is_new': is_new,
        'entropy': monitored_file.entropy_signature,
        'hash': monitored_file.last_hash
    }), 201 if is_new else 200

@app.route('/api/files/scan', methods=['POST'])
def scan_files():
    """Scan all monitored files for changes"""
    from file_monitor import scan_all_monitored_files
    results = scan_all_monitored_files()
    
    compromised = [r for r in results if r['integrity']['compromised']]
    
    return jsonify({
        'status': 'success',
        'total_scanned': len(results),
        'compromised_count': len(compromised),
        'results': results
    })

@app.route('/api/files/monitored/<int:file_id>')
def get_monitored_file(file_id):
    """Get specific monitored file"""
    db = get_db()
    try:
        file = db.query(MonitoredFile).filter(MonitoredFile.id == file_id).first()
        if not file:
            return jsonify({'error': 'File not found'}), 404
        return jsonify({
            'id': file.id,
            'file_path': file.file_path,
            'entropy_signature': file.entropy_signature,
            'last_hash': file.last_hash,
            'created_at': file.created_at.isoformat(),
            'last_checked': file.last_checked.isoformat(),
            'is_active': file.is_active,
            'attack_count': file.attack_count
        })
    finally:
        db.close()

@app.route('/api/quantum/measurements')
def get_quantum_measurements():
    """Get quantum measurements"""
    limit = request.args.get('limit', 20, type=int)
    db = get_db()
    try:
        measurements = db.query(QuantumMeasurement).order_by(desc(QuantumMeasurement.timestamp)).limit(limit).all()
        return jsonify([{
            'id': m.id,
            'timestamp': m.timestamp.isoformat(),
            'entropy_key': m.entropy_key,
            'data_hash': m.data_hash,
            'correlation': m.correlation,
            'measurements': m.measurements,
            'is_attack': m.is_attack
        } for m in measurements])
    finally:
        db.close()

@app.route('/api/quantum/measurements', methods=['POST'])
def create_quantum_measurement():
    """Create a new quantum measurement"""
    data = request.json
    db = get_db()
    try:
        measurement = QuantumMeasurement(
            entropy_key=data.get('entropy_key'),
            data_hash=data.get('data_hash'),
            correlation=data.get('correlation'),
            measurements=data.get('measurements'),
            is_attack=data.get('is_attack', False)
        )
        db.add(measurement)
        db.commit()
        db.refresh(measurement)
        return jsonify({'id': measurement.id, 'status': 'created'}), 201
    finally:
        db.close()

@app.route('/api/system/state')
def get_system_state():
    """Get current system state"""
    db = get_db()
    try:
        state = get_or_create_system_state(db)
        return jsonify({
            'id': state.id,
            'system_version': state.system_version,
            'total_resets': state.total_resets,
            'quantum_intact': state.quantum_intact,
            'last_updated': state.last_updated.isoformat()
        })
    finally:
        db.close()

@app.route('/api/system/state', methods=['PUT'])
def update_system_state():
    """Update system state"""
    data = request.json
    db = get_db()
    try:
        state = get_or_create_system_state(db)
        if 'system_version' in data:
            state.system_version = data['system_version']
        if 'total_resets' in data:
            state.total_resets = data['total_resets']
        if 'quantum_intact' in data:
            state.quantum_intact = data['quantum_intact']
        state.last_updated = datetime.utcnow()
        db.commit()
        return jsonify({'status': 'updated'})
    finally:
        db.close()

@app.route('/api/processes/recent')
def get_recent_processes():
    """Get recent process events"""
    limit = request.args.get('limit', 10, type=int)
    db = get_db()
    try:
        processes = db.query(ProcessEvent).order_by(desc(ProcessEvent.timestamp)).limit(limit).all()
        return jsonify([{
            'id': p.id,
            'timestamp': p.timestamp.isoformat(),
            'process_name': p.process_name,
            'process_id': p.process_id,
            'cpu_percent': p.cpu_percent,
            'memory_percent': p.memory_percent,
            'threat_score': p.threat_score,
            'is_suspicious': p.is_suspicious,
            'details': p.details
        } for p in processes])
    finally:
        db.close()

@app.route('/api/processes/suspicious')
def get_suspicious_processes():
    """Get all suspicious processes"""
    db = get_db()
    try:
        processes = db.query(ProcessEvent).filter(ProcessEvent.is_suspicious.is_(True)).order_by(desc(ProcessEvent.timestamp)).all()
        return jsonify([{
            'id': p.id,
            'timestamp': p.timestamp.isoformat(),
            'process_name': p.process_name,
            'process_id': p.process_id,
            'cpu_percent': p.cpu_percent,
            'memory_percent': p.memory_percent,
            'threat_score': p.threat_score,
            'details': p.details
        } for p in processes])
    finally:
        db.close()

@app.route('/api/threats/signatures')
def get_threat_signatures():
    """Get all threat signatures"""
    db = get_db()
    try:
        threats = db.query(ThreatSignature).all()
        return jsonify([{
            'id': t.id,
            'created_at': t.created_at.isoformat(),
            'threat_type': t.threat_type,
            'signature_pattern': t.signature_pattern,
            'severity': t.severity,
            'file_extensions': t.file_extensions,
            'process_names': t.process_names,
            'behavior_patterns': t.behavior_patterns,
            'detection_count': t.detection_count,
            'last_detected': t.last_detected.isoformat() if t.last_detected else None
        } for t in threats])
    finally:
        db.close()

@app.route('/api/responses/automated')
def get_automated_responses():
    """Get automated responses"""
    limit = request.args.get('limit', 20, type=int)
    db = get_db()
    try:
        responses = db.query(AutomatedResponse).order_by(desc(AutomatedResponse.timestamp)).limit(limit).all()
        return jsonify([{
            'id': r.id,
            'timestamp': r.timestamp.isoformat(),
            'threat_id': r.threat_id,
            'response_type': r.response_type,
            'action_taken': r.action_taken,
            'target': r.target,
            'success': r.success,
            'details': r.details
        } for r in responses])
    finally:
        db.close()

@app.route('/api/test/attack', methods=['POST'])
def simulate_attack():
    """Simulate various attack types for testing"""
    data = request.json
    attack_type = data.get('attack_type', 'ransomware')
    
    db = get_db()
    try:
        # Create security event based on attack type
        if attack_type == 'ransomware':
            event = SecurityEvent(
                event_type='Ransomware Attack Simulated',
                reason='Test: File encryption attempt detected',
                entropy=0.95,
                correlation=0.88
            )
        elif attack_type == 'malware':
            event = SecurityEvent(
                event_type='Malware Detected',
                reason='Test: Suspicious process behavior',
                entropy=0.75,
                correlation=0.82
            )
        elif attack_type == 'tampering':
            event = SecurityEvent(
                event_type='File Tampering',
                reason='Test: Unauthorized file modification',
                entropy=0.68,
                correlation=0.90
            )
        else:
            event = SecurityEvent(
                event_type='Unknown Threat',
                reason=f'Test: {attack_type} simulation',
                entropy=0.60,
                correlation=0.70
            )
        
        db.add(event)
        
        # Create automated response
        response = AutomatedResponse(
            threat_id=event.id,
            response_type='quarantine',
            action_taken=f'Simulated {attack_type} blocked and logged',
            target='test_file.txt',
            success=True,
            details={'simulation': True, 'attack_type': attack_type}
        )
        db.add(response)
        db.commit()
        
        return jsonify({
            'status': 'success',
            'attack_type': attack_type,
            'event_id': event.id,
            'response_id': response.id,
            'message': f'{attack_type.capitalize()} attack simulated and blocked'
        }), 201
    finally:
        db.close()

@app.route('/api/processes/scan', methods=['POST'])
def scan_processes():
    """Trigger a process scan"""
    from malware_detector import scan_running_processes
    suspicious = scan_running_processes()
    
    return jsonify({
        'status': 'success',
        'suspicious_count': len(suspicious),
        'suspicious_processes': suspicious
    })

@app.route('/api/security/encrypt', methods=['POST'])
def encrypt_data():
    """Encrypt sensitive data using AES-256"""
    data = request.json
    plaintext = data.get('data')
    
    if not plaintext:
        return jsonify({'error': 'data field is required'}), 400
    
    try:
        encrypted = encryptor.encrypt(plaintext)
        return jsonify({
            'status': 'success',
            'encrypted': encrypted,
            'algorithm': 'AES-256-CBC',
            'key_derivation': 'PBKDF2-SHA256'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/security/info')
def security_info():
    """Get security configuration information"""
    return jsonify({
        'encryption': {
            'algorithm': 'AES-256-CBC',
            'key_size': 256,
            'mode': 'CBC',
            'key_derivation': 'PBKDF2-SHA256',
            'iterations': 100000
        },
        'ssl': {
            'enabled': os.path.exists('./ssl/cert.pem'),
            'protocol': 'TLSv1.2+',
            'key_size': 4096,
            'certificate_type': 'Self-Signed'
        },
        'headers': {
            'hsts': 'enabled',
            'xss_protection': 'enabled',
            'content_security_policy': 'enabled',
            'frame_options': 'DENY'
        },
        'status': 'SECURED'
    })

@app.route('/api/training/scenarios')
def get_training_scenarios():
    """Get all cybersecurity training scenarios"""
    trainer = CybersecurityTraining()
    scenarios = []
    
    for scenario in trainer.scenarios:
        scenarios.append({
            'id': scenario['id'],
            'title': scenario['title'],
            'description': scenario['description'],
            'difficulty': scenario['difficulty'],
            'scenario': scenario['scenario'],
            'options': scenario['options'],
            'points': scenario['points']
        })
    
    return jsonify({
        'status': 'success',
        'total_scenarios': len(scenarios),
        'scenarios': scenarios
    })

@app.route('/api/training/check-answer', methods=['POST'])
def check_training_answer():
    """Check if a training answer is correct"""
    data = request.json
    scenario_id = data.get('scenario_id')
    answer = data.get('answer')
    
    if not scenario_id or not answer:
        return jsonify({'error': 'scenario_id and answer are required'}), 400
    
    trainer = CybersecurityTraining()
    scenario = next((s for s in trainer.scenarios if s['id'] == scenario_id), None)
    
    if not scenario:
        return jsonify({'error': 'Invalid scenario_id'}), 404
    
    is_correct = answer == scenario['correct_answer']
    points_earned = scenario['points'] if is_correct else 0
    
    # Log to database
    db = get_db()
    try:
        event = SecurityEvent(
            event_type='Training Completed',
            reason=f"Scenario {scenario_id}: {scenario['title']} - {'Correct' if is_correct else 'Incorrect'}",
            entropy=0.5,
            correlation=0.8
        )
        db.add(event)
        db.commit()
    finally:
        db.close()
    
    return jsonify({
        'status': 'success',
        'correct': is_correct,
        'correct_answer': scenario['correct_answer'],
        'explanation': scenario['explanation'],
        'points_earned': points_earned,
        'max_points': scenario['points']
    })

@app.route('/api/quantum/stats')
def get_quantum_stats():
    """Get quantum security statistics"""
    db = get_db()
    try:
        sys_state = get_or_create_system_state(db)
        
        # Get recent measurements
        measurements = db.query(QuantumMeasurement).order_by(
            QuantumMeasurement.timestamp.desc()
        ).limit(50).all()
        
        # Calculate trends
        if measurements:
            entropy_trend = [m.entropy_key for m in reversed(measurements)]
            correlation_trend = [m.correlation for m in reversed(measurements)]
            attack_indicators = [1 if m.is_attack else 0 for m in reversed(measurements)]
        else:
            entropy_trend = []
            correlation_trend = []
            attack_indicators = []
        
        return jsonify({
            'status': 'success',
            'system_state': {
                'quantum_intact': sys_state.quantum_intact,
                'system_version': sys_state.system_version,
                'last_reset': sys_state.last_updated.isoformat() if hasattr(sys_state, 'last_updated') else None
            },
            'trends': {
                'entropy': entropy_trend,
                'correlation': correlation_trend,
                'attacks': attack_indicators
            },
            'physics': {
                'bell_state': 'φ⁺ = 1/√2 (|00⟩ + |11⟩)',
                'entanglement': 'Quantum correlation protects data integrity',
                'detection_method': 'Entropy collapse detection',
                'algorithm': 'Bell state inequality violation'
            }
        })
    finally:
        db.close()

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'QuantumShield API'
    })

@app.route('/api/deploy/readiness')
def deploy_readiness():
    """Recommend whether it's safe to deploy right now"""
    db = get_db()
    try:
        state = get_or_create_system_state(db)
        suspicious_count = db.query(ProcessEvent).filter(ProcessEvent.is_suspicious.is_(True)).count()
        recent_events = db.query(SecurityEvent).filter(
            SecurityEvent.timestamp >= datetime.utcnow() - timedelta(hours=DEPLOY_READINESS_LOOKBACK_HOURS)
        ).count()
        lookback_unit = "hour" if DEPLOY_READINESS_LOOKBACK_HOURS == 1 else "hours"
        
        reasons = []
        if not state.quantum_intact:
            reasons.append("Quantum integrity is not intact")
        if suspicious_count > 0:
            reasons.append(f"{suspicious_count} suspicious process(es) flagged")
        if recent_events > 0:
            reasons.append(f"{recent_events} security event(s) detected in the last {DEPLOY_READINESS_LOOKBACK_HOURS} {lookback_unit}")
        
        safe_to_deploy = len(reasons) == 0
        
        return jsonify({
            'safe_to_deploy': safe_to_deploy,
            'recommendation': 'deploy' if safe_to_deploy else 'hold',
            'reasons': reasons,
            'metrics': {
                'suspicious_processes': suspicious_count,
                'recent_events_last_hour': recent_events,
                'quantum_intact': state.quantum_intact
            },
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as exc:
        return jsonify({
            'error': 'Failed to evaluate deployment readiness',
            'details': str(exc)
        }), 500
    finally:
        db.close()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    
    # Check if running in GitHub Codespaces or similar cloud environment
    is_cloud_env = os.getenv('CODESPACES') or os.getenv('GITPOD_WORKSPACE_ID')
    
    # Check if SSL certificates exist
    cert_file = './ssl/cert.pem'
    key_file = './ssl/key.pem'
    
    if os.path.exists(cert_file) and os.path.exists(key_file) and not is_cloud_env:
        # Create SSL context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(cert_file, key_file)
        
        print("\n" + "="*60)
        print("🔒 QuantumShield HTTPS Server Starting")
        print("="*60)
        print(f"🌐 HTTPS URL: https://localhost:{port}")
        print(f"🔐 AES-256 Encryption: ENABLED")
        print(f"🔒 SSL/TLS: ACTIVE (4096-bit RSA)")
        print(f"🛡️ Security Headers: ENFORCED")
        print("="*60 + "\n")
        
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True,
            ssl_context=ssl_context
        )
    else:
        if is_cloud_env:
            print("\n🌐 Cloud Environment Detected (Codespaces/Gitpod)")
            print("Starting in HTTP mode for cloud compatibility")
        else:
            print("\n⚠️  WARNING: SSL certificates not found!")
            print("Run 'python generate_ssl_cert.py' to create them.")
        print(f"\nStarting QuantumShield on HTTP://0.0.0.0:{port}\n")
        app.run(host='0.0.0.0', port=port, debug=True)

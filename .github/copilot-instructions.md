# QuantumShield - Copilot Instructions

## Project Overview

QuantumShield is a quantum entanglement-based self-healing security system that provides defense-in-depth protection as a secondary security layer. The system uses quantum computing principles (specifically Bell State |φ⁺⟩ entanglement) to detect and respond to security threats.

**Key Features:**
- Quantum entanglement security monitoring with Bell State circuits
- File integrity monitoring with entropy-based signatures
- Malware detection through process scanning
- Ransomware detection and protection
- Automated threat response and system self-healing
- Persistent data storage with SQLAlchemy (PostgreSQL/SQLite)
- Dual interface: Streamlit and Flask web applications

**Purpose:** This is a backup security layer that activates when primary device defenses (OS security, antivirus, firewalls) are compromised.

## Tech Stack and Frameworks

- **Languages:** Python 3.11+
- **Quantum Computing:** Qiskit 2.x, Qiskit Aer
- **Web Frameworks:** 
  - Streamlit 1.51+ (interactive UI)
  - Flask 3.0+ (traditional web interface)
- **Database:** SQLAlchemy 2.0+ with PostgreSQL (production) and SQLite (fallback/testing)
- **Visualization:** Matplotlib, Plotly
- **System Monitoring:** psutil 7.1+
- **Package Manager:** uv (preferred) or pip

## Architecture and Key Files

### Backend Core (Shared by both UIs)
- `database.py` - Database models and connection management
  - Supports both PostgreSQL (via DATABASE_URL env var) and SQLite (fallback)
  - Models: SecurityEvent, QuantumMeasurement, SystemState, MonitoredFile, ProcessEvent, AutomatedResponse
- `file_monitor.py` - File integrity monitoring with entropy-based checksums
- `malware_detector.py` - Process scanning and malware detection
- `ransomware_detector.py` - Ransomware detection and protection

### Frontend Applications
- `app.py` - Streamlit interface (port 8501)
- `flask_app.py` - Flask routes and API endpoints (port 5000)
- `templates/` - Flask HTML templates (base.html, index.html, file_monitor.html, threat_detection.html)

### Configuration
- `pyproject.toml` - Project dependencies
- `uv.lock` - Dependency lock file

## Coding Standards and Conventions

### Python Style
- Follow PEP 8 guidelines
- Use descriptive variable names
- Prefer explicit over implicit
- Use type hints where appropriate but not required (existing code doesn't consistently use them)
- Keep functions focused and single-purpose

### Database Conventions
- Always use SQLAlchemy ORM, never raw SQL
- Use the `get_db()` context manager for database sessions
- Commit explicitly after modifications
- Handle exceptions gracefully with try/except blocks
- Log database errors using the logging module

### Quantum Circuit Conventions
- Use Qiskit's QuantumCircuit for all quantum operations
- Bell State implementation: |φ⁺⟩ = 1/√2 (|00⟩ + |11⟩)
- Use Aer simulator for quantum measurements
- Store quantum measurements in the database with entropy keys

### Error Handling
- Use try/except blocks for file operations, database queries, and quantum operations
- Log errors using Python's logging module
- Return sensible defaults or None on errors (e.g., entropy = 0.0 for unreadable files)
- Don't let exceptions crash the application - handle them gracefully

### File Organization
- Group related functions together
- Keep database models in database.py
- Keep domain logic (monitoring, detection) in separate modules
- Templates follow Flask conventions in templates/ directory

## Database Configuration

### Environment Variables
- `DATABASE_URL` - PostgreSQL connection string (e.g., "postgresql://user:password@host:port/database")
- If not set, automatically falls back to SQLite: `quantum_security.db`

### Database Initialization
- Always call `init_db()` at application startup
- Creates all tables if they don't exist
- Safe to call multiple times (idempotent)

### Session Management
- Use `get_db()` context manager: `db = get_db()`
- Always close sessions properly (context manager handles this)
- Don't share sessions across requests

## Testing and Development

### Running the Applications
**Streamlit (Default):**
```bash
streamlit run app.py
```

**Flask:**
```bash
python flask_app.py
```

**Both can run simultaneously on different ports**

### Dependencies Installation
```bash
# Preferred (using uv)
uv sync

# Alternative (using pip)
pip install -e .
```

### No Formal Test Suite
- This project currently has no automated tests
- Manual testing is done through the web interfaces
- When adding features, test manually through both Streamlit and Flask interfaces
- Verify database persistence by checking stored records

### Database Testing
- Use SQLite for local development (no DATABASE_URL needed)
- For PostgreSQL testing, set DATABASE_URL environment variable
- Check database logs for connection issues

## Security and Performance Guidelines

### Security Best Practices
- **Never commit secrets** - Database URLs and credentials go in environment variables
- **Validate file paths** - Always check file existence before operations
- **Sanitize inputs** - Especially for file paths and process IDs
- **Use parameterized queries** - SQLAlchemy ORM handles this
- **Process termination** - Only terminate processes with explicit user confirmation

### Performance Considerations
- **Quantum circuits** - Keep circuit depth reasonable (current implementation is optimized)
- **File entropy calculation** - Can be slow for large files, consider caching
- **Process scanning** - Don't scan too frequently, can impact system performance
- **Database queries** - Use filters and limits to avoid loading excessive data
- **Visualization** - Pre-render complex quantum visualizations, don't regenerate on every request

### Quantum-Specific Security
- Quantum measurements are non-deterministic by design
- Store measurement results with entropy signatures for verification
- Self-healing mechanism resets quantum state when correlation breaks
- System version increments on each self-healing cycle

## Framework-Specific Instructions

### Streamlit (app.py)
- Use `st.session_state` for maintaining state across reruns
- Call `init_db()` once at module level
- Use `st.expander()` for detailed information sections
- Prefer `st.columns()` for layout
- Use `st.success()`, `st.warning()`, `st.error()` for user feedback
- Cache expensive operations with `@st.cache_data` or `@st.cache_resource`

### Flask (flask_app.py)
- Follow RESTful conventions for API endpoints
- Return JSON for API endpoints, render templates for pages
- Use Bootstrap 5 for consistent styling (already included in base.html)
- Handle POST requests with proper error responses
- Use Flask's `jsonify()` for JSON responses

### SQLAlchemy (database.py)
- All models inherit from `Base`
- Use `Column` types: Integer, String, Float, DateTime, Boolean, Text, JSON
- Add indexes on frequently queried fields
- Use `default=datetime.utcnow` for timestamp fields (not `datetime.utcnow()`)
- Implement `__repr__()` for better debugging

### Qiskit Quantum Operations
- Use `QuantumCircuit` with explicit register creation
- Measure to classical registers for result extraction
- Use `Aer.get_backend('statevector_simulator')` for state visualization
- Use `Aer.get_backend('qasm_simulator')` for measurement simulations
- Run circuits with sufficient shots (1000+ for statistical significance)

## Common Patterns and Idioms

### Adding a New Security Event
```python
from database import get_db, SecurityEvent
from datetime import datetime

db = get_db()
event = SecurityEvent(
    event_type="your_event_type",
    reason="Description of what happened",
    entropy=calculated_entropy,
    correlation=calculated_correlation,
    system_version=current_version
)
db.add(event)
db.commit()
```

### File Monitoring Pattern
```python
from file_monitor import add_monitored_file, scan_all_monitored_files

# Add file
file_obj, is_new = add_monitored_file("/path/to/file")

# Scan for changes
tampered_files = scan_all_monitored_files()
```

### Quantum Measurement Pattern
```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer

qr = QuantumRegister(2, 'q')
cr = ClassicalRegister(2, 'c')
qc = QuantumCircuit(qr, cr)

# Create Bell State
qc.h(qr[0])
qc.cx(qr[0], qr[1])

# Measure
qc.measure(qr, cr)

# Execute
simulator = Aer.get_backend('qasm_simulator')
job = simulator.run(qc, shots=1024)
result = job.result()
counts = result.get_counts(qc)
```

## Documentation Requirements

### Code Comments
- Add docstrings to new functions explaining purpose, parameters, and return values
- Comment complex quantum operations or mathematical calculations
- Explain security-critical logic
- Document environment variable requirements

### README Updates
- Update FLASK_README.md for Flask-related changes
- No main README.md currently exists - don't create one unless specifically requested
- Keep documentation concise and practical

## References and Resources

- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Qiskit Bell State Tutorial](https://learn.qiskit.org/course/ch-gates/entangled-states)
- [SQLAlchemy ORM Documentation](https://docs.sqlalchemy.org/en/20/orm/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Session State](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)

## Important Notes for Copilot

1. **This is a quantum security demonstration project** - It uses real quantum computing principles but is primarily educational/proof-of-concept
2. **Defense-in-depth philosophy** - Always respect that this is a secondary/backup security layer
3. **Dual interface support** - Changes to core logic should work in both Streamlit and Flask interfaces
4. **Database flexibility** - Code must work with both PostgreSQL and SQLite
5. **No breaking changes to quantum logic** - The Bell State implementation is core to the system
6. **Preserve logging** - Security events should be logged for audit trails
7. **User safety first** - Process termination and file operations need user confirmation
8. **Quantum non-determinism** - Embrace probabilistic results, don't force deterministic behavior

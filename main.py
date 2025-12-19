#!/usr/bin/env python3
"""
QuantumShield - Quantum Entanglement Self-Healing Security System

This is the main entry point for the QuantumShield application.
You can run either the Streamlit or Flask version of the application.
"""

import sys
import os
import subprocess


def print_banner():
    """Print application banner"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         🔐 QuantumShield Security System 🔐                   ║
║   Quantum Entanglement Self-Healing Security System          ║
║   Bell State |φ⁺⟩ = 1/√2 (|00⟩ + |11⟩)                      ║
╚═══════════════════════════════════════════════════════════════╝
    """)


def print_usage():
    """Print usage information"""
    print("\nUsage: python main.py [streamlit|flask]\n")
    print("Options:")
    print("  streamlit  - Run the Streamlit web interface (recommended)")
    print("  flask      - Run the Flask web application")
    print("\nIf no option is provided, the Streamlit app will run by default.\n")


def run_streamlit():
    """Run the Streamlit application"""
    print("\n🚀 Starting Streamlit application...")
    print("📍 URL: http://localhost:8501")
    print("💡 Press Ctrl+C to stop the application\n")
    
    try:
        subprocess.run(["streamlit", "run", "app.py", "--server.port", "8501"])
    except KeyboardInterrupt:
        print("\n\n✅ Application stopped successfully!")
    except FileNotFoundError:
        print("\n❌ Error: Streamlit is not installed!")
        print("💡 Install with: pip install streamlit")
        sys.exit(1)


def run_flask():
    """Run the Flask application"""
    print("\n🚀 Starting Flask application...")
    print("📍 URL: http://localhost:5000")
    print("💡 Press Ctrl+C to stop the application\n")
    
    try:
        subprocess.run([sys.executable, "flask_app.py"])
    except KeyboardInterrupt:
        print("\n\n✅ Application stopped successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point for QuantumShield application"""
    print_banner()
    
    # Determine which app to run
    if len(sys.argv) > 1:
        app_choice = sys.argv[1].lower()
        
        if app_choice in ['-h', '--help', 'help']:
            print_usage()
            return
        elif app_choice == 'streamlit':
            run_streamlit()
        elif app_choice == 'flask':
            run_flask()
        else:
            print(f"❌ Unknown option: {app_choice}")
            print_usage()
            sys.exit(1)
    else:
        # Default to Streamlit
        print("ℹ️  No option provided, starting Streamlit app (default)")
        print("💡 Run 'python main.py help' for more options\n")
        run_streamlit()


if __name__ == "__main__":
    main()

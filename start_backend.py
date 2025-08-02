#!/usr/bin/env python3
"""
Start script for GPTravel FastAPI backend
"""

import sys
import subprocess
import os
import shutil

def check_poetry():
    """Check if Poetry is available"""
    if shutil.which("poetry") is None:
        print("❌ Poetry not found")
        print("Please install Poetry: https://python-poetry.org/docs/#installation")
        return False
    print("✅ Poetry found")
    return True

def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI dependencies found")
        return True
    except ImportError:
        print("❌ FastAPI dependencies missing")
        print("Installing dependencies with Poetry...")
        try:
            subprocess.run(["poetry", "install"], check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("Please run: poetry install")
            return False

def start_server():
    """Start the FastAPI server"""
    if not check_poetry():
        sys.exit(1)
        
    if not check_requirements():
        sys.exit(1)
    
    print("🚀 Starting GPTravel FastAPI Backend...")
    print("📍 Server will be available at: http://127.0.0.1:8000")
    print("📖 API Documentation at: http://127.0.0.1:8000/docs")
    print("🔧 Use Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start uvicorn server using Poetry
        subprocess.run([
            "poetry", "run", "uvicorn",
            "backend_api:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n👋 GPTravel backend stopped")
    except FileNotFoundError:
        print("❌ Poetry not found. Please install Poetry first.")
        print("Alternative: python -m uvicorn backend_api:app --host 127.0.0.1 --port 8000 --reload")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Try running: poetry install")
        sys.exit(1)

if __name__ == "__main__":
    start_server() 

#!/usr/bin/env python3
"""
INTENTRA-X Launcher for MacBook M4 Pro
Optimized for Apple Silicon
"""

import subprocess
import time
import sys
import os
import signal

def main():
    print("🚀 INTENTRA-X Launcher for MacBook M4 Pro")
    print("=" * 60)
    
    brain_process = None
    dashboard_process = None
    
    try:
        # Start the brain
        print("\n🧠 Starting INTENTRA-X Brain (Mock AirSim)...")
        brain_process = subprocess.Popen(
            [sys.executable, "main_brain.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"   Brain started (PID: {brain_process.pid})")
        
        # Wait for brain to initialize
        print("   Initializing...")
        time.sleep(3)
        
        # Check if brain is still running
        if brain_process.poll() is not None:
            print("   ⚠️  Brain process exited early")
            stdout, stderr = brain_process.communicate()
            print(f"   Output: {stdout}")
            print(f"   Error: {stderr}")
            return
        
        print("   ✓ Brain running")
        
        # Start the dashboard
        print("\n📊 Starting Dashboard...")
        print("\n" + "=" * 60)
        print("  🌐 Dashboard URL: http://localhost:8501")
        print("  📍 Select 'Live' mode in sidebar for mock data")
        print("=" * 60)
        print("\n⌨️  Press Ctrl+C to stop\n")
        
        dashboard_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "dashboard_clean.py"],
            env={**os.environ, "STREAMLIT_SERVER_HEADLESS": "true"}
        )
        
        # Wait for dashboard to finish (blocks until Ctrl+C)
        dashboard_process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down INTENTRA-X...")
    
    finally:
        # Cleanup
        if brain_process and brain_process.poll() is None:
            print("   Stopping brain...")
            brain_process.terminate()
            try:
                brain_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                brain_process.kill()
        
        if dashboard_process and dashboard_process.poll() is None:
            print("   Stopping dashboard...")
            dashboard_process.terminate()
            try:
                dashboard_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                dashboard_process.kill()
        
        print("✓ Stopped\n")

if __name__ == "__main__":
    main()

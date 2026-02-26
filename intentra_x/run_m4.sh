#!/bin/bash
# INTENTRA-X Launcher for MacBook M4 Pro
# Runs both brain and dashboard with mock AirSim

echo "🚀 Starting INTENTRA-X on MacBook M4 Pro..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Kill any existing processes
pkill -f "python main_brain.py" 2>/dev/null
pkill -f "streamlit run dashboard.py" 2>/dev/null
sleep 1

# Start the brain in background
echo "🧠 Starting INTENTRA-X Brain (Mock AirSim)..."
python main_brain.py > brain.log 2>&1 &
BRAIN_PID=$!
echo "   Brain PID: $BRAIN_PID"

# Wait for brain to initialize
sleep 3

# Start the dashboard
echo "📊 Starting Dashboard..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Dashboard will open at: http://localhost:8501"
echo "  Select 'Live' mode in the sidebar to see mock data"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop both processes"
echo ""

# Run streamlit (this will block)
streamlit run dashboard.py

# Cleanup on exit
echo ""
echo "🛑 Stopping INTENTRA-X..."
kill $BRAIN_PID 2>/dev/null
pkill -f "python main_brain.py" 2>/dev/null
echo "✓ Stopped"

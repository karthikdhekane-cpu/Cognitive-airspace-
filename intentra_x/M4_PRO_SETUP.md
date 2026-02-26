# INTENTRA-X for MacBook M4 Pro

## Quick Start (3 Steps)

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Run the System
```bash
python run_m4.py
```

### 3. Open Dashboard
Open your browser to: **http://localhost:8502**

In the sidebar, select **"Live"** mode to see the mock AirSim data.

---

## What's Running

The `run_m4.py` launcher starts two processes:

1. **Brain Process** (`main_brain.py`)
   - Runs mock AirSim simulation
   - Generates realistic drone telemetry
   - Performs intent classification
   - Calculates risk scores
   - Writes data to `live_output.json`

2. **Dashboard Process** (`dashboard.py`)
   - Streamlit web interface
   - Reads live data from `live_output.json`
   - Displays real-time visualizations
   - Shows risk heatmaps and trajectories

---

## Alternative: Shell Script

You can also use the bash script:
```bash
./run_m4.sh
```

---

## Alternative: Manual Start

If you prefer to run processes separately:

**Terminal 1 - Brain:**
```bash
source venv/bin/activate
python main_brain.py
```

**Terminal 2 - Dashboard:**
```bash
source venv/bin/activate
streamlit run dashboard.py
```

Then open http://localhost:8501 and select "Live" mode.

---

## Stopping the System

Press `Ctrl+C` in the terminal where you ran `run_m4.py`

Both processes will stop automatically.

---

## Features

✅ **No AirSim Required** - Uses mock simulation  
✅ **Apple Silicon Optimized** - Native M4 Pro support  
✅ **Real-time Visualization** - Live dashboard updates  
✅ **Intent Classification** - LSTM neural network  
✅ **Risk Assessment** - Multi-factor risk engine  
✅ **State Machine** - Autonomous behavior switching  
✅ **Counterfactual Predictions** - Future risk projection  

---

## Dashboard Controls

**Sidebar:**
- Mode: Select "Live" for mock AirSim data
- Auto-refresh: Enable for real-time updates
- Refresh rate: Adjust update frequency

**Visualizations:**
- Altitude & Speed gauges
- Intent classification with confidence
- Risk score meter
- 2D trajectory map with heatmap
- Time-series graphs
- State transition log

---

## Troubleshooting

### Port Already in Use
If you see "Address already in use":
```bash
# Kill existing streamlit processes
pkill -f streamlit

# Then restart
python run_m4.py
```

### Brain Not Generating Data
Check if `live_output.json` is being updated:
```bash
ls -lh live_output.json
```

If the file is old or missing, restart the brain process.

### Dashboard Shows "No Live Data"
1. Make sure brain process is running
2. Check that `live_output.json` exists
3. Select "Live" mode in dashboard sidebar
4. Enable auto-refresh

---

## Performance Tips

**For M4 Pro:**
- The system is optimized for Apple Silicon
- No additional configuration needed
- Runs smoothly with default settings

**If experiencing lag:**
- Reduce refresh rate in dashboard sidebar
- Close other browser tabs
- Check Activity Monitor for CPU usage

---

## File Structure

```
intentra_x/
├── run_m4.py              ← Main launcher (use this!)
├── run_m4.sh              ← Alternative bash launcher
├── main_brain.py          ← Brain with mock AirSim
├── dashboard.py           ← Streamlit dashboard
├── mock_airsim.py         ← Mock AirSim client
├── live_output.json       ← Live data (auto-generated)
└── venv/                  ← Virtual environment
```

---

## What Makes This M4 Pro Compatible?

1. **No AirSim Dependency** - Mock simulation runs natively
2. **Python-based** - No Windows-specific binaries
3. **Lightweight** - Optimized for laptop performance
4. **Native Libraries** - All dependencies support ARM64

---

## Next Steps

- Explore the dashboard visualizations
- Watch state transitions in real-time
- Modify risk thresholds in `main_brain.py`
- Customize behaviors in `state_machine.py`
- Add new features to the dashboard

---

## Support

If you encounter issues:
1. Check that virtual environment is activated
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Check process logs: `cat brain.log` (if using shell script)
4. Restart the system: `Ctrl+C` then `python run_m4.py`

---

**Enjoy your autonomous drone intelligence system! 🚁🧠**

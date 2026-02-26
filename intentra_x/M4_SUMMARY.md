# ✅ INTENTRA-X - M4 Pro Ready

## What Was Done

Your INTENTRA-X system is now fully configured and running on MacBook M4 Pro with mock AirSim integration.

### Changes Made:

1. **Modified `main_brain.py`**
   - Added mock AirSim support
   - Falls back to mock when real AirSim unavailable
   - Simulates realistic drone behavior
   - Generates live telemetry data

2. **Created M4 Pro Launchers**
   - `run_m4.py` - Python launcher (recommended)
   - `run_m4.sh` - Bash script alternative
   - Both handle process management automatically

3. **Added Documentation**
   - `M4_PRO_SETUP.md` - Complete setup guide
   - `START_HERE.txt` - Quick reference
   - This summary document

---

## Current Status: ✅ RUNNING

**Brain Process:** Active (PID: 18835)
- Generating mock telemetry
- Writing to `live_output.json`
- Simulating drone flight

**Dashboard:** Active
- URL: http://localhost:8502
- Streamlit interface ready
- Waiting for you to open it

---

## How to Use Right Now

1. **Open your browser**
2. **Go to:** http://localhost:8502
3. **In sidebar:** Select "Live" mode
4. **Enable:** Auto-refresh toggle
5. **Watch:** Real-time drone simulation!

---

## What You'll See

### Dashboard Features:
- **Left Panel:** Altitude & speed gauges, intent classification
- **Center:** 2D trajectory map with risk heatmap
- **Right Panel:** Risk breakdown, counterfactual predictions
- **Bottom:** Time-series graphs (risk, intent, altitude)
- **State Log:** Real-time state transitions

### Mock Simulation:
- Drone starts at position (0, 0, 20m altitude)
- Moves based on current state (TRANSIT/SURVEILLANCE/ADAPTIVE)
- Risk engine evaluates position and trajectory
- LSTM classifies intent from movement patterns
- State machine switches behaviors based on risk

---

## To Stop

Press `Ctrl+C` in the terminal where `run_m4.py` is running.

Both processes will stop cleanly.

---

## To Restart

```bash
source venv/bin/activate
python run_m4.py
```

---

## Architecture

```
┌─────────────────┐
│   main_brain.py │  ← Runs mock AirSim simulation
│   (Mock AirSim) │     Generates telemetry
└────────┬────────┘     Classifies intent
         │              Calculates risk
         ↓
┌─────────────────┐
│live_output.json │  ← JSON file with live data
└────────┬────────┘     Updated every 0.5 seconds
         │
         ↓
┌─────────────────┐
│  dashboard.py   │  ← Streamlit web interface
│   (Port 8502)   │     Reads JSON file
└─────────────────┘     Displays visualizations
```

---

## Key Files

| File | Purpose |
|------|---------|
| `run_m4.py` | Main launcher - use this to start |
| `main_brain.py` | Brain with mock AirSim integration |
| `mock_airsim.py` | Mock AirSim client |
| `dashboard.py` | Streamlit dashboard |
| `live_output.json` | Live data (auto-generated) |
| `M4_PRO_SETUP.md` | Detailed setup guide |

---

## Why This Works on M4 Pro

✅ **No Windows Dependencies** - Pure Python  
✅ **No Real AirSim** - Mock simulation  
✅ **ARM64 Compatible** - All libraries support Apple Silicon  
✅ **Lightweight** - Optimized for laptop performance  
✅ **Native** - No emulation or compatibility layers  

---

## Next Steps

1. **Open the dashboard** (http://localhost:8502)
2. **Explore the visualizations**
3. **Watch state transitions**
4. **Modify parameters** in `main_brain.py`
5. **Customize dashboard** in `dashboard.py`

---

## Demo Mode vs Live Mode

**Demo Mode:**
- Built into dashboard
- Generates synthetic data
- No brain process needed
- Good for UI testing

**Live Mode:** ← You're using this!
- Reads from `live_output.json`
- Uses brain process with mock AirSim
- Real intent classification
- Real risk assessment
- Real state machine

---

## Performance

On M4 Pro, you should see:
- Smooth dashboard updates
- No lag or stuttering
- Low CPU usage (~5-10%)
- Instant state transitions

If you experience issues, reduce the refresh rate in the dashboard sidebar.

---

## Success! 🎉

Your INTENTRA-X system is fully operational on MacBook M4 Pro.

**Current Status:** Both processes running  
**Dashboard:** http://localhost:8502  
**Mode:** Live with Mock AirSim  

Just open the URL and start exploring!

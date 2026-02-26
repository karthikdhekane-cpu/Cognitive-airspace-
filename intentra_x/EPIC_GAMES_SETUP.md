# INTENTRA-X with Epic Games (Unreal Engine)

## Overview

INTENTRA-X now supports both:
- **Epic Games (Unreal Engine + AirSim)** - Full 3D simulation with realistic physics
- **Mock AirSim** - Lightweight Python simulation (no Unreal needed)

The system automatically detects which is available and connects accordingly.

---

## Quick Start (Current Setup)

Your system is already configured to work with Mock AirSim. To run:

```bash
source venv/bin/activate
python run_m4.py
```

This will use Mock AirSim by default (no Epic Games/Unreal needed).

---

## Adding Epic Games Support

If you want to use the full Unreal Engine simulation:

### Step 1: Install Unreal Engine

**Option A: Epic Games Launcher (Recommended)**
1. Download Epic Games Launcher: https://www.epicgames.com/store/download
2. Install Unreal Engine 4.27 or 5.x
3. Create a new project or use existing one

**Option B: Build from Source**
1. Clone Unreal Engine from GitHub
2. Follow build instructions for macOS

### Step 2: Install AirSim

**Clone AirSim:**
```bash
cd ~/Documents
git clone https://github.com/Microsoft/AirSim.git
cd AirSim
```

**Build AirSim for macOS:**
```bash
./setup.sh
./build.sh
```

**Install Python Client:**
```bash
pip install airsim
```

### Step 3: Configure AirSim

Create settings file at `~/Documents/AirSim/settings.json`:

```json
{
  "SettingsVersion": 1.2,
  "SimMode": "Multirotor",
  "ClockSpeed": 1,
  "ViewMode": "SpringArmChase",
  "Vehicles": {
    "Drone1": {
      "VehicleType": "SimpleFlight",
      "X": 0, "Y": 0, "Z": -2,
      "Yaw": 0
    }
  },
  "CameraDefaults": {
    "CaptureSettings": [
      {
        "ImageType": 0,
        "Width": 1920,
        "Height": 1080,
        "FOV_Degrees": 90
      }
    ]
  }
}
```

### Step 4: Launch Unreal + AirSim

1. Open your Unreal project
2. Load the AirSim plugin
3. Press Play in Unreal Editor
4. Wait for simulation to start

### Step 5: Run INTENTRA-X

```bash
source venv/bin/activate
python run_m4.py
```

The system will automatically detect Epic Games and connect!

---

## How It Works

### Automatic Detection

The `SimulationBridge` class tries to connect in this order:

1. **Epic Games (Unreal + AirSim)** - If available
2. **Mock AirSim** - Python fallback
3. **Offline Mode** - Data playback only

### Connection Priority

```python
# Prefer Epic Games
brain = IntentRAXBrain(prefer_epic=True)

# Prefer Mock (current default)
brain = IntentRAXBrain(prefer_epic=False)
```

### Checking Connection

The system prints which simulation it's using:

```
🎮 Using Epic Games (Unreal Engine + AirSim)
```

or

```
🐍 Using Mock AirSim (Python Simulation)
```

---

## Features by Simulation Type

### Epic Games (Unreal Engine)

✅ Full 3D graphics  
✅ Realistic physics  
✅ Camera images  
✅ Collision detection  
✅ Weather effects  
✅ Multiple environments  
✅ GPU acceleration  

### Mock AirSim

✅ No installation needed  
✅ Lightweight  
✅ Fast startup  
✅ Works on any Mac  
✅ No GPU required  
✅ Perfect for testing  

---

## Architecture

```
┌─────────────────────────────────────┐
│     INTENTRA-X Brain                │
│     (main_brain.py)                 │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│   Simulation Bridge                 │
│   (simulation_bridge.py)            │
│   - Auto-detection                  │
│   - Unified interface               │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        ↓             ↓
┌──────────────┐  ┌──────────────┐
│ Epic Games   │  │ Mock AirSim  │
│ (Unreal +    │  │ (Python)     │
│  AirSim)     │  │              │
└──────────────┘  └──────────────┘
```

---

## Testing the Bridge

Test which simulation is available:

```bash
python simulation_bridge.py
```

This will:
1. Try to connect to Epic Games
2. Fall back to Mock if unavailable
3. Run a test flight
4. Show telemetry data

---

## Switching Between Simulations

### Use Epic Games (if available)

```bash
# Edit main_brain.py, line ~280
brain = IntentRAXBrain(simulation_mode=True, prefer_epic=True)
```

### Force Mock AirSim

```bash
# Edit main_brain.py, line ~280
brain = IntentRAXBrain(simulation_mode=True, prefer_epic=False)
```

---

## Telemetry Comparison

### Epic Games Telemetry

```python
{
    'source': 'epic_games',
    'position': [x, y, z],
    'velocity': [vx, vy, vz],
    'altitude': alt,
    'speed': speed,
    'orientation': {'roll': r, 'pitch': p, 'yaw': y},
    'gps': {'latitude': lat, 'longitude': lon},
    'barometer': {'altitude': alt, 'pressure': p},
    'imu': {'angular_velocity': [...], 'linear_acceleration': [...]},
    'armed': True/False,
    'landed': True/False
}
```

### Mock AirSim Telemetry

```python
{
    'source': 'mock_airsim',
    'position': [x, y, z],
    'velocity': [vx, vy, vz],
    'altitude': alt,
    'speed': speed,
    'orientation': {'roll': r, 'pitch': p, 'yaw': y},
    'gps': {'latitude': lat, 'longitude': lon},
    'armed': True/False,
    'landed': True/False
}
```

Both formats are compatible with the dashboard!

---

## Troubleshooting

### Epic Games Not Detected

**Check AirSim is running:**
```bash
# Should show Unreal process
ps aux | grep -i unreal
```

**Check AirSim Python client:**
```bash
python -c "import airsim; print('AirSim installed')"
```

**Check connection:**
```bash
python -c "import airsim; c = airsim.MultirotorClient(); c.confirmConnection(); print('Connected')"
```

### Falls Back to Mock

This is normal if:
- Unreal Engine not running
- AirSim not installed
- Connection failed

The system will work fine with Mock AirSim!

### Performance Issues (Epic Games)

- Lower Unreal graphics settings
- Reduce resolution
- Close other applications
- Check GPU usage in Activity Monitor

---

## Recommended Setup

### For Development/Testing
Use **Mock AirSim** - fast, lightweight, no setup

### For Presentations/Demos
Use **Epic Games** - impressive visuals, realistic physics

### For Competition
Use **Epic Games** if available, **Mock AirSim** as backup

---

## Camera Images (Epic Games Only)

When using Epic Games, you can capture camera images:

```python
# In main_brain.py
image = brain.simulation_bridge.get_camera_image()
```

This feature is not available in Mock AirSim.

---

## Current Status

Your system is configured to:
- ✅ Try Epic Games first
- ✅ Fall back to Mock AirSim
- ✅ Work out of the box with Mock
- ✅ Auto-upgrade to Epic when available

No changes needed unless you want to install Epic Games!

---

## Summary

| Feature | Epic Games | Mock AirSim |
|---------|-----------|-------------|
| Installation | Complex | None |
| Graphics | 3D/Realistic | None |
| Physics | Realistic | Simplified |
| Camera | Yes | No |
| Speed | Slower | Fast |
| M4 Pro | Yes | Yes |
| Setup Time | Hours | Seconds |
| Best For | Demos | Development |

---

**Current Recommendation:** Stick with Mock AirSim for now. It works perfectly and requires no setup. Add Epic Games later if you need the visual wow factor!

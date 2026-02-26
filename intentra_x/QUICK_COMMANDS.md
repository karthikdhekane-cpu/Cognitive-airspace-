# Quick Commands Reference

## Start System
```bash
source venv/bin/activate
python run_m4.py
```

## Stop System
Press `Ctrl+C` in the terminal

## Check Status
```bash
# Check if processes are running
ps aux | grep -E "(main_brain|streamlit)" | grep -v grep

# Check live data file
ls -lh live_output.json
tail -20 live_output.json
```

## Access Dashboard
```
http://localhost:8502
```

## Restart System
```bash
# Stop current processes
pkill -f "main_brain"
pkill -f "streamlit"

# Start again
source venv/bin/activate
python run_m4.py
```

## View Logs (if using shell script)
```bash
tail -f brain.log
```

## Manual Start (Two Terminals)

**Terminal 1:**
```bash
source venv/bin/activate
python main_brain.py
```

**Terminal 2:**
```bash
source venv/bin/activate
streamlit run dashboard.py
```

## Troubleshooting

**Port busy:**
```bash
pkill -f streamlit
lsof -ti:8502 | xargs kill -9
```

**Clean restart:**
```bash
pkill -f "main_brain"
pkill -f "streamlit"
rm live_output.json
python run_m4.py
```

**Check Python version:**
```bash
python --version  # Should be 3.8+
```

**Reinstall dependencies:**
```bash
pip install -r requirements.txt
```

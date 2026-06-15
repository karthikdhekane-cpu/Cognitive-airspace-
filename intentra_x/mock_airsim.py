"""
Mock AirSim Client for INTENTRA-X Dashboard
Provides simulated telemetry data for testing
"""

import random
import time
from datetime import datetime

class MockAirSimClient:
    def __init__(self):
        self.connected = True
        self.start_time = time.time()
    
    def connect(self):
        self.connected = True
        return True
    
    def confirmConnection(self):
        """Mock confirmConnection for compatibility"""
        self.connected = True
        return True
    def getMultirotorState(self):
        class Position:
            x_val = random.uniform(-50, 50)
            y_val = random.uniform(-50, 50)
            z_val = -random.uniform(10, 30)

        class Velocity:
            x_val = random.uniform(-5, 5)
            y_val = random.uniform(-5, 5)
            z_val = random.uniform(-1, 1)

        class Kinematics:
            position = Position()
            linear_velocity = Velocity()

        class State:
            kinematics_estimated = Kinematics()

        return State()
    
    def disconnect(self):
        self.connected = False
    
    def get_telemetry(self):
        """Generate mock telemetry data"""
        elapsed = time.time() - self.start_time
        
        return {
            'timestamp': datetime.now().isoformat(),
            'altitude': 100 + random.uniform(-5, 5),
            'speed': 25 + random.uniform(-3, 3),
            'battery': max(20, 100 - elapsed * 0.1),
            'gps_lat': 47.6062 + random.uniform(-0.001, 0.001),
            'gps_lon': -122.3321 + random.uniform(-0.001, 0.001),
            'heading': random.uniform(0, 360),
            'pitch': random.uniform(-5, 5),
            'roll': random.uniform(-5, 5),
            'connected': self.connected
        }

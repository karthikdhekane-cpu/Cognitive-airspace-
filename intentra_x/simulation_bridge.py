"""
INTENTRA-X Simulation Bridge
Connects to Epic Games (Unreal Engine + AirSim) or Mock AirSim
Provides unified interface for both real and simulated environments
"""

import numpy as np
import time
import json
from datetime import datetime
from enum import Enum

class SimulationType(Enum):
    EPIC_GAMES = "epic_games"  # Unreal Engine + AirSim
    MOCK_AIRSIM = "mock_airsim"  # Pure Python simulation
    OFFLINE = "offline"  # No simulation, data playback only

class SimulationBridge:
    """
    Unified interface for Epic Games (Unreal) and Mock AirSim
    Automatically detects and connects to available simulation
    """
    
    def __init__(self, prefer_epic=True):
        self.simulation_type = None
        self.client = None
        self.mock_state = {
            'position': [0.0, 0.0, -20.0],
            'velocity': [5.0, 0.0, 0.0],
            'orientation': [0.0, 0.0, 0.0],  # roll, pitch, yaw
            'angular_velocity': [0.0, 0.0, 0.0],
            'time': 0.0,
            'armed': False,
            'airborne': False
        }
        
        # Try to connect in order of preference
        if prefer_epic:
            if self._try_connect_epic():
                return
        
        if self._try_connect_mock():
            return
        
        # Fallback to offline mode
        self.simulation_type = SimulationType.OFFLINE
        print("⚠️  No simulation available - running in offline mode")
    
    def _try_connect_epic(self):
        """Try to connect to Epic Games (Unreal Engine + AirSim)"""
        try:
            import airsim
            print("🎮 Attempting to connect to Epic Games (Unreal Engine)...")
            
            client = airsim.MultirotorClient()
            client.confirmConnection()
            client.enableApiControl(True)
            
            self.client = client
            self.simulation_type = SimulationType.EPIC_GAMES
            print("✓ Connected to Epic Games (Unreal Engine + AirSim)")
            print(f"  Server Version: {client.getServerVersion()}")
            print(f"  Client Version: {client.getClientVersion()}")
            return True
            
        except ImportError:
            print("  AirSim library not installed")
            return False
        except Exception as e:
            print(f"  Epic Games connection failed: {e}")
            return False
    
    def _try_connect_mock(self):
        """Connect to Mock AirSim (Python simulation)"""
        try:
            from mock_airsim import MockAirSimClient
            self.client = MockAirSimClient()
            self.simulation_type = SimulationType.MOCK_AIRSIM
            print("✓ Connected to Mock AirSim (Python simulation)")
            return True
        except Exception as e:
            print(f"  Mock AirSim connection failed: {e}")
            return False
    
    def get_simulation_info(self):
        """Get information about current simulation"""
        return {
            'type': self.simulation_type.value if self.simulation_type else 'none',
            'connected': self.client is not None,
            'epic_games': self.simulation_type == SimulationType.EPIC_GAMES,
            'mock': self.simulation_type == SimulationType.MOCK_AIRSIM,
            'offline': self.simulation_type == SimulationType.OFFLINE
        }
    
    def arm(self):
        """Arm the drone"""
        if self.simulation_type == SimulationType.EPIC_GAMES:
            self.client.armDisarm(True)
            self.mock_state['armed'] = True
            print("✓ Armed (Epic Games)")
        elif self.simulation_type == SimulationType.MOCK_AIRSIM:
            self.mock_state['armed'] = True
            print("✓ Armed (Mock)")
        return True
    
    def disarm(self):
        """Disarm the drone"""
        if self.simulation_type == SimulationType.EPIC_GAMES:
            self.client.armDisarm(False)
            self.mock_state['armed'] = False
            print("✓ Disarmed (Epic Games)")
        elif self.simulation_type == SimulationType.MOCK_AIRSIM:
            self.mock_state['armed'] = False
            print("✓ Disarmed (Mock)")
        return True
    
    def takeoff(self, altitude=10):
        """Takeoff to specified altitude"""
        if self.simulation_type == SimulationType.EPIC_GAMES:
            print("🚁 Taking off (Epic Games)...")
            self.client.takeoffAsync().join()
            self.client.moveToZAsync(-altitude, 2).join()
            self.mock_state['airborne'] = True
            print(f"✓ Airborne at {altitude}m")
            
        elif self.simulation_type == SimulationType.MOCK_AIRSIM:
            print("🚁 Taking off (Mock)...")
            self.mock_state['position'] = [0.0, 0.0, -altitude]
            self.mock_state['airborne'] = True
            print(f"✓ Airborne at {altitude}m (simulated)")
        
        return True
    
    def land(self):
        """Land the drone"""
        if self.simulation_type == SimulationType.EPIC_GAMES:
            print("🛬 Landing (Epic Games)...")
            self.client.landAsync().join()
            self.mock_state['airborne'] = False
            print("✓ Landed")
            
        elif self.simulation_type == SimulationType.MOCK_AIRSIM:
            print("🛬 Landing (Mock)...")
            self.mock_state['position'][2] = 0
            self.mock_state['airborne'] = False
            print("✓ Landed (simulated)")
        
        return True
    
    def get_telemetry(self):
        """Get current telemetry from simulation"""
        if self.simulation_type == SimulationType.EPIC_GAMES:
            return self._get_epic_telemetry()
        elif self.simulation_type == SimulationType.MOCK_AIRSIM:
            return self._get_mock_telemetry()
        else:
            return self._get_offline_telemetry()
    
    def _get_epic_telemetry(self):
        """Get telemetry from Epic Games (Unreal Engine)"""
        import airsim
        
        state = self.client.getMultirotorState()
        pos = state.kinematics_estimated.position
        vel = state.kinematics_estimated.linear_velocity
        orientation = state.kinematics_estimated.orientation
        
        # Convert quaternion to Euler angles
        roll, pitch, yaw = airsim.to_eularian_angles(orientation)
        
        # Get GPS data
        gps = self.client.getGpsData()
        
        # Get barometer data
        baro = self.client.getBarometerData()
        
        # Get IMU data
        imu = self.client.getImuData()
        
        telemetry = {
            'timestamp': time.time(),
            'source': 'epic_games',
            'position': [pos.x_val, pos.y_val, pos.z_val],
            'velocity': [vel.x_val, vel.y_val, vel.z_val],
            'altitude': -pos.z_val,  # NED coordinates
            'speed': np.linalg.norm([vel.x_val, vel.y_val, vel.z_val]),
            'orientation': {
                'roll': np.degrees(roll),
                'pitch': np.degrees(pitch),
                'yaw': np.degrees(yaw)
            },
            'gps': {
                'latitude': gps.gnss.geo_point.latitude,
                'longitude': gps.gnss.geo_point.longitude,
                'altitude': gps.gnss.geo_point.altitude
            },
            'barometer': {
                'altitude': baro.altitude,
                'pressure': baro.pressure
            },
            'imu': {
                'angular_velocity': [
                    imu.angular_velocity.x_val,
                    imu.angular_velocity.y_val,
                    imu.angular_velocity.z_val
                ],
                'linear_acceleration': [
                    imu.linear_acceleration.x_val,
                    imu.linear_acceleration.y_val,
                    imu.linear_acceleration.z_val
                ]
            },
            'armed': state.armed,
            'landed': state.landed_state == airsim.LandedState.Landed
        }
        
        return telemetry
    
    def _get_mock_telemetry(self):
        """Get telemetry from Mock AirSim"""
        self.mock_state['time'] += 0.5
        
        # Simulate realistic movement
        dt = 0.5
        self.mock_state['position'][0] += self.mock_state['velocity'][0] * dt
        self.mock_state['position'][1] += self.mock_state['velocity'][1] * dt
        self.mock_state['position'][2] += self.mock_state['velocity'][2] * dt
        
        # Add some noise for realism
        noise = np.random.randn(3) * 0.1
        
        telemetry = {
            'timestamp': time.time(),
            'source': 'mock_airsim',
            'position': [
                self.mock_state['position'][0] + noise[0],
                self.mock_state['position'][1] + noise[1],
                self.mock_state['position'][2] + noise[2]
            ],
            'velocity': self.mock_state['velocity'].copy(),
            'altitude': -self.mock_state['position'][2],
            'speed': np.linalg.norm(self.mock_state['velocity']),
            'orientation': {
                'roll': self.mock_state['orientation'][0],
                'pitch': self.mock_state['orientation'][1],
                'yaw': self.mock_state['orientation'][2]
            },
            'gps': {
                'latitude': 35.0522 + self.mock_state['position'][0] / 111000,
                'longitude': -106.6056 + self.mock_state['position'][1] / 111000,
                'altitude': -self.mock_state['position'][2]
            },
            'armed': self.mock_state['armed'],
            'landed': not self.mock_state['airborne']
        }
        
        return telemetry
    
    def _get_offline_telemetry(self):
        """Get dummy telemetry for offline mode"""
        return {
            'timestamp': time.time(),
            'source': 'offline',
            'position': [0, 0, 0],
            'velocity': [0, 0, 0],
            'altitude': 0,
            'speed': 0,
            'armed': False,
            'landed': True
        }
    
    def move_by_velocity(self, vx, vy, vz, duration=1.0):
        """Move drone by velocity"""
        if self.simulation_type == SimulationType.EPIC_GAMES:
            import airsim
            self.client.moveByVelocityAsync(
                vx, vy, vz, 
                duration=duration,
                drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom
            )
        elif self.simulation_type == SimulationType.MOCK_AIRSIM:
            self.mock_state['velocity'] = [vx, vy, vz]
    
    def move_to_position(self, x, y, z, velocity=5.0):
        """Move drone to position"""
        if self.simulation_type == SimulationType.EPIC_GAMES:
            self.client.moveToPositionAsync(x, y, z, velocity)
        elif self.simulation_type == SimulationType.MOCK_AIRSIM:
            # Calculate velocity direction
            current = self.mock_state['position']
            direction = np.array([x - current[0], y - current[1], z - current[2]])
            distance = np.linalg.norm(direction)
            if distance > 0:
                direction = direction / distance * velocity
                self.mock_state['velocity'] = direction.tolist()
    
    def hover(self):
        """Hover in place"""
        if self.simulation_type == SimulationType.EPIC_GAMES:
            self.client.hoverAsync().join()
        elif self.simulation_type == SimulationType.MOCK_AIRSIM:
            self.mock_state['velocity'] = [0, 0, 0]
    
    def reset(self):
        """Reset simulation"""
        if self.simulation_type == SimulationType.EPIC_GAMES:
            self.client.reset()
            print("✓ Epic Games simulation reset")
        elif self.simulation_type == SimulationType.MOCK_AIRSIM:
            self.mock_state = {
                'position': [0.0, 0.0, -20.0],
                'velocity': [5.0, 0.0, 0.0],
                'orientation': [0.0, 0.0, 0.0],
                'angular_velocity': [0.0, 0.0, 0.0],
                'time': 0.0,
                'armed': False,
                'airborne': False
            }
            print("✓ Mock simulation reset")
    
    def get_camera_image(self, camera_name="0", image_type=0):
        """Get camera image (Epic Games only)"""
        if self.simulation_type == SimulationType.EPIC_GAMES:
            import airsim
            responses = self.client.simGetImages([
                airsim.ImageRequest(camera_name, image_type, False, False)
            ])
            return responses[0] if responses else None
        return None
    
    def disconnect(self):
        """Disconnect from simulation"""
        if self.simulation_type == SimulationType.EPIC_GAMES:
            self.client.enableApiControl(False)
            print("✓ Disconnected from Epic Games")
        elif self.simulation_type == SimulationType.MOCK_AIRSIM:
            print("✓ Disconnected from Mock AirSim")
        
        self.client = None
        self.simulation_type = None


def test_simulation_bridge():
    """Test the simulation bridge"""
    print("\n" + "="*60)
    print("Testing INTENTRA-X Simulation Bridge")
    print("="*60 + "\n")
    
    # Create bridge (will auto-detect)
    bridge = SimulationBridge(prefer_epic=True)
    
    # Show simulation info
    info = bridge.get_simulation_info()
    print(f"\nSimulation Type: {info['type']}")
    print(f"Connected: {info['connected']}")
    print(f"Epic Games: {info['epic_games']}")
    print(f"Mock: {info['mock']}")
    
    # Test basic operations
    if info['connected']:
        print("\n--- Testing Basic Operations ---")
        bridge.arm()
        bridge.takeoff(altitude=20)
        
        print("\n--- Testing Telemetry ---")
        for i in range(5):
            telemetry = bridge.get_telemetry()
            print(f"Position: {telemetry['position']}")
            print(f"Altitude: {telemetry['altitude']:.2f}m")
            print(f"Speed: {telemetry['speed']:.2f}m/s")
            print(f"Source: {telemetry['source']}")
            print()
            time.sleep(1)
        
        bridge.land()
        bridge.disarm()
    
    bridge.disconnect()
    print("\n✓ Test complete")


if __name__ == "__main__":
    test_simulation_bridge()

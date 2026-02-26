"""
INTENTRA-X Main Brain
Cognitive Airspace Intelligence & Risk-Aware Autonomous Drone System

ETHICAL NOTICE:
- This system is for SAFETY and AWARENESS only
- No stealth, evasion, or invisibility logic
- Decision-support tool for risk assessment
- Explainable AI with full transparency
- Designed for research and competition use
"""

import numpy as np
import time
import json
from datetime import datetime
from state_machine import StateMachine, DroneState
from feature_extractor import FeatureExtractor
from lstm_model import IntentClassifier
from risk_engine import RiskEngine
from uncertainty import UncertaintyEstimator
from counterfactual import CounterfactualEngine
from telemetry_logger import TelemetryLogger
from simulation_bridge import SimulationBridge, SimulationType

class IntentRAXBrain:
    """Main control system for autonomous drone with cognitive intelligence"""
    
    def __init__(self, simulation_mode=True, prefer_epic=True):
        self.simulation_mode = simulation_mode
        self.simulation_bridge = None
        self.state_machine = StateMachine()
        self.feature_extractor = FeatureExtractor()
        self.intent_model = IntentClassifier()
        self.risk_engine = RiskEngine()
        self.uncertainty_estimator = UncertaintyEstimator()
        self.counterfactual = CounterfactualEngine()
        self.logger = TelemetryLogger()
        
        # Trajectory history
        self.trajectory = []
        self.max_trajectory_length = 100
        
        # Behavior parameters
        self.transit_speed = 5.0
        self.surveillance_radius = 15.0
        self.surveillance_altitude = -20.0
        self.risk_threshold = 0.7
        
        if simulation_mode:
            self.connect_simulation(prefer_epic=prefer_epic)
    
    def connect_simulation(self, prefer_epic=True):
        """Connect to simulation (Epic Games or Mock)"""
        self.simulation_bridge = SimulationBridge(prefer_epic=prefer_epic)
        
        info = self.simulation_bridge.get_simulation_info()
        if info['epic_games']:
            print("🎮 Using Epic Games (Unreal Engine + AirSim)")
        elif info['mock']:
            print("🐍 Using Mock AirSim (Python Simulation)")
        else:
            print("⚠️  No simulation available")
            self.simulation_mode = False
    
    def get_telemetry(self):
        """Extract current drone telemetry"""
        if not self.simulation_bridge:
            return None
        
        telemetry_raw = self.simulation_bridge.get_telemetry()
        
        # Normalize telemetry format
        telemetry = {
            'timestamp': telemetry_raw['timestamp'],
            'position': telemetry_raw['position'],
            'velocity': telemetry_raw['velocity'],
            'altitude': telemetry_raw['altitude'],
            'speed': telemetry_raw['speed'],
            'yaw': telemetry_raw.get('orientation', {}).get('yaw', 0)
        }
        
        return telemetry
    
    def execute_transit(self):
        """Execute transit behavior - straight line movement"""
        if not self.simulation_bridge:
            return
        
        self.simulation_bridge.move_by_velocity(
            self.transit_speed, 0, 0, duration=1.0
        )
    
    def execute_surveillance(self, center_x=0, center_y=0):
        """Execute surveillance behavior - circular loitering pattern"""
        if not self.simulation_bridge:
            return
        
        # Circular path around point of interest
        t = time.time()
        angle = (t % 20) / 20 * 2 * np.pi  # 20 second orbit
        
        target_x = center_x + self.surveillance_radius * np.cos(angle)
        target_y = center_y + self.surveillance_radius * np.sin(angle)
        
        self.simulation_bridge.move_to_position(
            target_x, target_y, self.surveillance_altitude, velocity=3
        )
    
    def execute_adaptive(self, risk_breakdown):
        """Execute adaptive behavior - risk mitigation"""
        if not self.simulation_bridge:
            return
        
        # ETHICAL NOTE: This is risk AWARENESS, not evasion
        # System adapts to maintain safety margins
        
        current_pos = self.get_telemetry()['position']
        
        # If too close to high-risk zone, increase altitude
        if risk_breakdown.get('proximity_risk', 0) > 0.5:
            target_z = current_pos[2] - 5  # Go higher (NED coords)
            self.simulation_bridge.move_to_position(
                current_pos[0], current_pos[1], target_z, velocity=2
            )
        else:
            # Slow, deliberate movement
            self.simulation_bridge.move_by_velocity(2, 0, 0, duration=1.0)
    
    def update_trajectory(self, position):
        """Maintain trajectory history"""
        self.trajectory.append(position)
        if len(self.trajectory) > self.max_trajectory_length:
            self.trajectory.pop(0)
    
    def run_cycle(self):
        """Execute one intelligence cycle"""
        # Get current telemetry
        telemetry = self.get_telemetry()
        if not telemetry:
            return None
        
        self.update_trajectory(telemetry['position'])
        
        # Extract behavioral features
        features = self.feature_extractor.extract(self.trajectory, telemetry)
        
        # Classify intent using LSTM
        intent_result = self.intent_model.predict(features)
        intent_label = intent_result['label']
        intent_probs = intent_result['probabilities']
        
        # Estimate uncertainty
        uncertainty = self.uncertainty_estimator.compute(intent_probs)
        
        # Compute risk
        risk_result = self.risk_engine.compute_risk(
            telemetry['position'],
            self.trajectory,
            telemetry['altitude']
        )
        
        # Predict counterfactual risk
        cf_risk = self.counterfactual.predict_future_risk(
            telemetry['position'],
            telemetry['velocity'],
            self.state_machine.current_state
        )
        
        # State machine decision
        self.state_machine.update(
            risk_result['risk_score'],
            uncertainty,
            self.risk_threshold
        )
        
        # Execute behavior based on state
        if self.state_machine.current_state == DroneState.TRANSIT:
            self.execute_transit()
        elif self.state_machine.current_state == DroneState.SURVEILLANCE:
            self.execute_surveillance()
        elif self.state_machine.current_state == DroneState.ADAPTIVE:
            self.execute_adaptive(risk_result['risk_breakdown'])
        
        # Compile output
        output = {
            'timestamp': telemetry['timestamp'],
            'position': telemetry['position'],
            'velocity': telemetry['velocity'],
            'altitude': telemetry['altitude'],
            'speed': telemetry['speed'],
            'trajectory': self.trajectory[-20:],  # Last 20 points
            'intent': intent_label,
            'intent_confidence': float(np.max(intent_probs)),
            'intent_probabilities': intent_probs.tolist(),
            'uncertainty': float(uncertainty),
            'risk_score': risk_result['risk_score'],
            'risk_breakdown': risk_result['risk_breakdown'],
            'risk_explanation': risk_result['explanation'],
            'state': self.state_machine.current_state.name,
            'counterfactual_risk': cf_risk,
            'state_history': self.state_machine.get_history()
        }
        
        # Log and save
        self.logger.log(output)
        self.save_live_output(output)
        
        return output
    
    def save_live_output(self, data):
        """Save current state to JSON for dashboard"""
        with open('live_output.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def takeoff(self):
        """Takeoff sequence"""
        if self.simulation_bridge:
            self.simulation_bridge.arm()
            self.simulation_bridge.takeoff(altitude=20)
    
    def land(self):
        """Landing sequence"""
        if self.simulation_bridge:
            self.simulation_bridge.land()
            self.simulation_bridge.disarm()

def main():
    """Main execution loop"""
    # Try Epic Games first, fall back to Mock
    brain = IntentRAXBrain(simulation_mode=True, prefer_epic=True)
    
    if brain.simulation_mode and brain.simulation_bridge:
        info = brain.simulation_bridge.get_simulation_info()
        
        brain.takeoff()
        
        try:
            if info['epic_games']:
                print("\n🎮 INTENTRA-X Brain Active (Epic Games / Unreal Engine)")
            else:
                print("\n🐍 INTENTRA-X Brain Active (Mock AirSim)")
            print("Press Ctrl+C to stop\n")
            
            while True:
                output = brain.run_cycle()
                if output:
                    sim_type = "🎮" if info['epic_games'] else "🐍"
                    print(f"{sim_type} State: {output['state']} | "
                          f"Intent: {output['intent']} ({output['intent_confidence']:.2f}) | "
                          f"Risk: {output['risk_score']:.2f} | "
                          f"Uncertainty: {output['uncertainty']:.2f}")
                
                time.sleep(0.5)
        
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            brain.land()
    else:
        print("Run in demo mode - check dashboard with sample data")

if __name__ == "__main__":
    main()

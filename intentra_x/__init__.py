"""
INTENTRA-X: Cognitive Airspace Intelligence & Risk-Aware Autonomous Drone System

A competition-grade autonomous drone intelligence platform combining:
- AirSim simulation
- PyTorch LSTM intent classification
- Multi-factor risk assessment
- Uncertainty quantification
- Counterfactual reasoning
- Mission-grade Streamlit dashboard

ETHICAL FRAMEWORK:
- Designed for SAFETY and AWARENESS
- No stealth or evasion capabilities
- Transparent, explainable AI
- Decision-support tool
- Full audit trail

Author: Competition Team
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "INTENTRA-X Team"

# Core modules
from .main_brain import IntentRAXBrain
from .state_machine import StateMachine, DroneState
from .environment import EnvironmentModel, CameraModel
from .feature_extractor import FeatureExtractor
from .lstm_model import IntentClassifier
from .risk_engine import RiskEngine
from .uncertainty import UncertaintyEstimator
from .counterfactual import CounterfactualEngine
from .heatmap_engine import HeatmapEngine
from .telemetry_logger import TelemetryLogger

__all__ = [
    'IntentRAXBrain',
    'StateMachine',
    'DroneState',
    'EnvironmentModel',
    'CameraModel',
    'FeatureExtractor',
    'IntentClassifier',
    'RiskEngine',
    'UncertaintyEstimator',
    'CounterfactualEngine',
    'HeatmapEngine',
    'TelemetryLogger'
]

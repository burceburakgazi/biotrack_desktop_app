from datetime import datetime
from typing import Dict

class BiometricReading:
    def __init__(self, timestamp: str, glucose: float, ph: float, oxygen: float):
        self.timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        self.glucose = glucose
        self.ph = ph
        self.oxygen = oxygen

    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'glucose': self.glucose,
            'ph': self.ph,
            'oxygen': self.oxygen
        }

class User:
    def __init__(self, uid: str, email: str, token: str):
        self.uid = uid
        self.email = email
        self.token = token
        self.login_time = datetime.now()

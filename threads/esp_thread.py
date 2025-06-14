import time
import requests
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from data.models import BiometricReading

class ESP32DataThread(QThread):
    data_received = pyqtSignal(BiometricReading)
    connection_status = pyqtSignal(bool)

    def __init__(self, ip_address: str):
        super().__init__()
        self.ip_address = ip_address
        self.running = True

    def run(self):
        while self.running:
            try:
                response = requests.get(f"http://{self.ip_address}/data", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    reading = BiometricReading(
                        data['timestamp'],
                        data['glucose'],
                        data['ph'],
                        data['oxygen']
                    )
                    self.data_received.emit(reading)
                    self.connection_status.emit(True)
                else:
                    self.connection_status.emit(False)
            except Exception:
                self.connection_status.emit(False)
            time.sleep(5)

    def stop(self):
        self.running = False


class FakeDataThread(QThread):
    data_received = pyqtSignal(BiometricReading)
    connection_status = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            now = datetime.now()
            fake_data = BiometricReading(
                timestamp=now.isoformat(),
                glucose=90 + (5 * (time.time() % 2)),
                ph=7.0 + (0.2 * (time.time() % 1)),
                oxygen=95 + (2 * (time.time() % 1))
            )
            self.data_received.emit(fake_data)
            self.connection_status.emit(False)  # Sahte veri, bağlantı yok
            time.sleep(5)

    def stop(self):
        self.running = False

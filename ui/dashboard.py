# ui/dashboard.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from data.database import DatabaseManager
from data.models import BiometricReading, User
from threads.esp_thread import ESP32DataThread, FakeDataThread
from ui.widgets import MetricCard, ChartWidget
from PyQt5.QtCore import Qt
import requests
from datetime import datetime

class DashboardWidget(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.esp32_thread = None
        self.current_user = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        self.status_label = QLabel("● Disconnected")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.last_update_label = QLabel("Last update: Never")
        self.last_update_label.setStyleSheet("color: #666;")

        header_layout.addWidget(self.status_label)
        header_layout.addStretch()
        header_layout.addWidget(self.last_update_label)

        metrics_layout = QHBoxLayout()
        self.glucose_card = MetricCard("Glucose", "mg/dL", "#ff6b6b")
        self.ph_card = MetricCard("pH Level", "pH", "#4ecdc4")
        self.oxygen_card = MetricCard("Oxygen", "%", "#45b7d1")

        metrics_layout.addWidget(self.glucose_card)
        metrics_layout.addWidget(self.ph_card)
        metrics_layout.addWidget(self.oxygen_card)

        self.glucose_chart = ChartWidget("Glucose Levels", "#ff6b6b")
        self.ph_chart = ChartWidget("pH Levels", "#4ecdc4")
        self.oxygen_chart = ChartWidget("Oxygen Levels", "#45b7d1")

        layout.addLayout(header_layout)
        layout.addLayout(metrics_layout)
        layout.addWidget(self.glucose_chart)
        layout.addWidget(self.ph_chart)
        layout.addWidget(self.oxygen_chart)

        self.setLayout(layout)

    def start_monitoring(self, user: User, esp32_ip: str):
        self.current_user = user

        if hasattr(self, 'esp32_thread') and self.esp32_thread:
            self.esp32_thread.stop()
            self.esp32_thread.wait()

        try:
            response = requests.get(f"http://{esp32_ip}/data", timeout=3)
            if response.status_code == 200:
                self.esp32_thread = ESP32DataThread(esp32_ip)
            else:
                raise Exception("ESP32 bağlantısı başarısız")
        except Exception:
            print("ESP32 bağlantısı yok, sahte veri kullanılacak.")
            self.esp32_thread = FakeDataThread()

        self.esp32_thread.data_received.connect(self.handle_new_data)
        self.esp32_thread.connection_status.connect(self.update_connection_status)
        self.esp32_thread.start()

    def handle_new_data(self, reading: BiometricReading):
        self.glucose_card.update_value(reading.glucose, self.get_glucose_status(reading.glucose))
        self.ph_card.update_value(reading.ph, self.get_ph_status(reading.ph))
        self.oxygen_card.update_value(reading.oxygen, self.get_oxygen_status(reading.oxygen))

        self.glucose_chart.add_data_point(reading.timestamp, reading.glucose)
        self.ph_chart.add_data_point(reading.timestamp, reading.ph)
        self.oxygen_chart.add_data_point(reading.timestamp, reading.oxygen)

        if self.current_user:
            self.db_manager.save_reading(self.current_user.uid, reading)

        self.last_update_label.setText(f"Last update: {reading.timestamp.strftime('%H:%M:%S')}")

    def update_connection_status(self, connected: bool):
        if connected:
            self.status_label.setText("● Connected")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.status_label.setText("● Disconnected")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")

    def get_glucose_status(self, value: float) -> str:
        if value < 70 or value > 140:
            return "critical"
        elif value < 80 or value > 120:
            return "warning"
        return "normal"

    def get_ph_status(self, value: float) -> str:
        if value < 6.5 or value > 7.5:
            return "critical"
        elif value < 7.0 or value > 7.4:
            return "warning"
        return "normal"

    def get_oxygen_status(self, value: float) -> str:
        if value < 90:
            return "critical"
        elif value < 95:
            return "warning"
        return "normal"

    def stop_monitoring(self):
        if self.esp32_thread:
            self.esp32_thread.stop()
            self.esp32_thread.wait()

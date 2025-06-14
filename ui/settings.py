# ui/settings.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLabel, QLineEdit, QSpinBox,
    QPushButton, QGridLayout, QMessageBox
)
from PyQt5.QtCore import QSettings
from config import CONFIG

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings(CONFIG['settings_file'], QSettings.IniFormat)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # ESP32 Configuration
        esp32_group = QGroupBox("ESP32 Configuration")
        esp32_layout = QGridLayout()

        esp32_layout.addWidget(QLabel("IP Address:"), 0, 0)
        self.esp32_ip_input = QLineEdit()
        self.esp32_ip_input.setText(self.settings.value('esp32_ip', CONFIG['esp32_default_ip']))
        esp32_layout.addWidget(self.esp32_ip_input, 0, 1)

        esp32_group.setLayout(esp32_layout)

        # Alert Thresholds
        alerts_group = QGroupBox("Alert Thresholds")
        alerts_layout = QGridLayout()

        alerts_layout.addWidget(QLabel("Glucose Min:"), 0, 0)
        self.glucose_min_spin = QSpinBox()
        self.glucose_min_spin.setRange(50, 150)
        self.glucose_min_spin.setValue(int(self.settings.value('glucose_min', 70)))
        alerts_layout.addWidget(self.glucose_min_spin, 0, 1)

        alerts_layout.addWidget(QLabel("Glucose Max:"), 0, 2)
        self.glucose_max_spin = QSpinBox()
        self.glucose_max_spin.setRange(100, 200)
        self.glucose_max_spin.setValue(int(self.settings.value('glucose_max', 140)))
        alerts_layout.addWidget(self.glucose_max_spin, 0, 3)

        alerts_layout.addWidget(QLabel("pH Min (x10):"), 1, 0)
        self.ph_min_spin = QSpinBox()
        self.ph_min_spin.setRange(60, 75)
        self.ph_min_spin.setValue(int(self.settings.value('ph_min', 65)))
        alerts_layout.addWidget(self.ph_min_spin, 1, 1)

        alerts_layout.addWidget(QLabel("pH Max (x10):"), 1, 2)
        self.ph_max_spin = QSpinBox()
        self.ph_max_spin.setRange(70, 80)
        self.ph_max_spin.setValue(int(self.settings.value('ph_max', 75)))
        alerts_layout.addWidget(self.ph_max_spin, 1, 3)

        alerts_layout.addWidget(QLabel("Oxygen Min:"), 2, 0)
        self.oxygen_min_spin = QSpinBox()
        self.oxygen_min_spin.setRange(85, 100)
        self.oxygen_min_spin.setValue(int(self.settings.value('oxygen_min', 90)))
        alerts_layout.addWidget(self.oxygen_min_spin, 2, 1)

        alerts_group.setLayout(alerts_layout)

        # Save Button
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setStyleSheet("background-color: #007bff; color: white;")
        self.save_btn.clicked.connect(self.save_settings)

        layout.addWidget(esp32_group)
        layout.addWidget(alerts_group)
        layout.addWidget(self.save_btn)
        layout.addStretch()
        self.setLayout(layout)

    def save_settings(self):
        self.settings.setValue('esp32_ip', self.esp32_ip_input.text())
        self.settings.setValue('glucose_min', self.glucose_min_spin.value())
        self.settings.setValue('glucose_max', self.glucose_max_spin.value())
        self.settings.setValue('ph_min', self.ph_min_spin.value())
        self.settings.setValue('ph_max', self.ph_max_spin.value())
        self.settings.setValue('oxygen_min', self.oxygen_min_spin.value())
        QMessageBox.information(self, "Success", "Settings saved successfully!")

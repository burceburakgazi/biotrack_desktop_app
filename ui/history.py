# ui/history.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QDateEdit, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox
)
from PyQt5.QtCore import QDate
from data.database import DatabaseManager
from data.models import User
from datetime import datetime

class HistoryWidget(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.current_user = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("From:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.start_date.setCalendarPopup(True)
        controls_layout.addWidget(self.start_date)

        controls_layout.addWidget(QLabel("To:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        controls_layout.addWidget(self.end_date)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_history)
        controls_layout.addWidget(self.refresh_btn)

        self.export_btn = QPushButton("Export CSV")
        self.export_btn.clicked.connect(self.export_data)
        controls_layout.addWidget(self.export_btn)

        controls_layout.addStretch()

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Timestamp", "Glucose", "pH", "Oxygen"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(controls_layout)
        layout.addWidget(self.history_table)
        self.setLayout(layout)

    def set_user(self, user: User):
        self.current_user = user
        self.load_history()

    def load_history(self):
        if not self.current_user:
            return

        start_dt = datetime.combine(self.start_date.date().toPyDate(), datetime.min.time())
        end_dt = datetime.combine(self.end_date.date().toPyDate(), datetime.max.time())
        readings = self.db_manager.get_readings(self.current_user.uid, start_dt, end_dt)

        self.history_table.setRowCount(len(readings))
        for i, reading in enumerate(readings):
            self.history_table.setItem(i, 0, QTableWidgetItem(reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')))
            self.history_table.setItem(i, 1, QTableWidgetItem(f"{reading.glucose:.1f}"))
            self.history_table.setItem(i, 2, QTableWidgetItem(f"{reading.ph:.2f}"))
            self.history_table.setItem(i, 3, QTableWidgetItem(f"{reading.oxygen:.1f}"))

    def export_data(self):
        if not self.current_user:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Data",
            f"biotrack_data_{datetime.now().strftime('%Y%m%d')}.csv",
            "CSV Files (*.csv)"
        )

        if filename:
            self.db_manager.export_to_csv(self.current_user.uid, filename)
            QMessageBox.information(self, "Success", f"Data exported to {filename}")

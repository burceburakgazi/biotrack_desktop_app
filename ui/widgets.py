# ui/widgets.py

from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates

class MetricCard(QFrame):
    def __init__(self, title: str, unit: str, color: str):
        super().__init__()
        self.title = title
        self.unit = unit
        self.color = color
        self.value = 0.0
        self.status = "normal"
        self.setup_ui()

    def setup_ui(self):
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {self.color};
                border-radius: 10px;
                padding: 10px;
            }}
        """)

        layout = QVBoxLayout()

        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        self.value_label = QLabel("--")
        self.value_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet(f"color: {self.color};")

        unit_label = QLabel(self.unit)
        unit_label.setFont(QFont("Arial", 10))
        unit_label.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("●")
        self.status_label.setFont(QFont("Arial", 16))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: green;")

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(unit_label)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def update_value(self, value: float, status: str = "normal"):
        self.value = value
        self.status = status
        self.value_label.setText(f"{value:.1f}")

        status_colors = {
            "normal": "green",
            "warning": "orange",
            "critical": "red"
        }

        self.status_label.setStyleSheet(f"color: {status_colors.get(status, 'green')};")


class ChartWidget(QWidget):
    def __init__(self, title: str, color: str):
        super().__init__()
        self.title = title
        self.color = color
        self.data_points = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.figure = Figure(figsize=(12, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.ax.set_title(self.title)
        self.ax.set_ylabel("Value")
        self.ax.grid(True, alpha=0.3)

        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def add_data_point(self, timestamp, value: float):
        self.data_points.append((timestamp, value))
        if len(self.data_points) > 100:
            self.data_points = self.data_points[-100:]
        self.update_chart()

    def update_chart(self):
        if not self.data_points:
            return

        timestamps, values = zip(*self.data_points)

        self.ax.clear()
        self.ax.plot(timestamps, values, color=self.color, linewidth=2)
        self.ax.set_title(self.title)
        self.ax.set_ylabel("Value")
        self.ax.grid(True, alpha=0.3)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.figure.autofmt_xdate()
        self.canvas.draw()

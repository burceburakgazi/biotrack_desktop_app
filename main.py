import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtGui import QIcon

from data.database import DatabaseManager
from auth.auth_service import AuthService
from ui.login import LoginWindow
from ui.dashboard import DashboardWidget
from ui.history import HistoryWidget
from ui.settings import SettingsWidget
from config import CONFIG

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(CONFIG['app_name'])
        self.setMinimumSize(1000, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.db_manager = DatabaseManager(CONFIG['db_name'])
        self.auth_service = AuthService()
        self.current_user = None

        self.login_window = LoginWindow(self.auth_service)
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()

    def on_login_success(self, user):
        self.current_user = user
        self.login_window.close()

        self.dashboard = DashboardWidget(self.db_manager)
        self.history = HistoryWidget(self.db_manager)
        self.settings = SettingsWidget()

        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.history, "History")
        self.tabs.addTab(self.settings, "Settings")

        self.dashboard.start_monitoring(user, CONFIG['esp32_default_ip'])
        self.history.set_user(user)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(CONFIG['app_name'])
    app.setApplicationVersion(CONFIG['version'])
    app.setWindowIcon(QIcon("resources/bioicon.png"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

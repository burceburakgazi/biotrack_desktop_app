from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from auth.auth_service import AuthService
from data.models import User

class LoginWindow(QWidget):
    login_successful = pyqtSignal(User)

    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("BioTrack SmartBand - Login")
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                font-family: 'Segoe UI';
            }
            QLineEdit {
                padding: 12px;
                border: 1.5px solid #ccc;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton {
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("BioTrack SmartBand")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #007bff;")

        subtitle = QLabel("Secure Patient Monitoring System")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; margin-bottom: 10px;")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Sign In")
        self.login_btn.setStyleSheet("background-color: #007bff; color: white;")
        self.login_btn.clicked.connect(self.handle_login)

        self.signup_btn = QPushButton("Create Account")
        self.signup_btn.setStyleSheet("background-color: #28a745; color: white;")
        self.signup_btn.clicked.connect(self.handle_signup)

        self.reset_btn = QPushButton("Forgot Password?")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #007bff;
                border: 1px solid #007bff;
            }
            QPushButton:hover {
                background-color: #007bff;
                color: white;
            }
        """)
        self.reset_btn.clicked.connect(self.handle_reset_password)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.signup_btn)
        layout.addWidget(self.reset_btn)

        self.setLayout(layout)

    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        success, message = self.auth_service.sign_in(email, password)
        if success:
            self.login_successful.emit(self.auth_service.current_user)
            self.close()
        else:
            QMessageBox.critical(self, "Login Failed", message)

    def handle_signup(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters")
            return

        success, message = self.auth_service.sign_up(email, password)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Registration Failed", message)

    def handle_reset_password(self):
        email = self.email_input.text()
        if not email:
            QMessageBox.warning(self, "Error", "Please enter your email address")
            return

        success, message = self.auth_service.reset_password(email)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)

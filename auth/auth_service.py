import requests
from typing import Optional, Tuple
from data.models import User

CONFIG = {
    'firebase_api_key': 'YOUR_KEY_HERE',
    'firebase_auth_url': 'https://identitytoolkit.googleapis.com/v1/accounts',
}

class AuthService:
    def __init__(self):
        self.api_key = CONFIG['firebase_api_key']
        self.auth_url = CONFIG['firebase_auth_url']
        self.current_user: Optional[User] = None

    def sign_up(self, email: str, password: str) -> Tuple[bool, str]:
        url = f"{self.auth_url}:signUp?key={self.api_key}"
        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            data = response.json()
            if response.status_code == 200:
                return True, "Account created successfully!"
            else:
                error_msg = data.get('error', {}).get('message', 'Registration failed')
                return False, error_msg
        except Exception as e:
            return False, f"Network error: {str(e)}"

    def sign_in(self, email: str, password: str) -> Tuple[bool, str]:
        url = f"{self.auth_url}:signInWithPassword?key={self.api_key}"
        payload = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            data = response.json()
            if response.status_code == 200:
                self.current_user = User(
                    uid=data['localId'],
                    email=data['email'],
                    token=data['idToken']
                )
                return True, "Login successful!"
            else:
                error_msg = data.get('error', {}).get('message', 'Login failed')
                return False, error_msg
        except Exception as e:
            return False, f"Network error: {str(e)}"

    def reset_password(self, email: str) -> Tuple[bool, str]:
        url = f"{self.auth_url}:sendOobCode?key={self.api_key}"
        payload = {
            'requestType': 'PASSWORD_RESET',
            'email': email
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return True, "Password reset email sent!"
            else:
                return False, "Failed to send reset email"
        except Exception as e:
            return False, f"Network error: {str(e)}"

    def is_authenticated(self) -> bool:
        return self.current_user is not None

    def logout(self):
        self.current_user = None

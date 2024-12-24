from typing import Dict
import json
import os

class AuthManager:
    def __init__(self):
        self.users_file = "users.json"
        self.users = self._load_users()

    def _load_users(self) -> Dict:
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)

    def save_token(self, user_id: str, token: str):
        self.users[str(user_id)] = token
        self._save_users()

    def get_token(self, user_id: str) -> str:
        return self.users.get(str(user_id))

    def remove_token(self, user_id: str):
        if str(user_id) in self.users:
            del self.users[str(user_id)]
            self._save_users()
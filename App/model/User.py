from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin):

    def __init__(self, username, email, user_type, password_hash=None):
        self.username = username
        self.email = email
        self.user_type = user_type
        self.password_hash = password_hash

    def __repr__(self):
        return f"User {self.username}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_type(self):
        return self.user_type

    def get_id(self):
        return self.email

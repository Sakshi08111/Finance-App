from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    """
    User model representing a user in the application.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """
        Hashes the password and stores it in the password_hash field.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the provided password matches the stored hash.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        String representation of the User object.
        """
        return f"<User {self.username}>"

class Transaction(db.Model):
    """
    Transaction model representing a financial transaction.
    """
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(50), nullable=False)
    source = db.Column(db.String(100), nullable=True)  # Optional for expenses
    category = db.Column(db.String(100), nullable=True)  # Optional for income
    description = db.Column(db.String(255), nullable=True)  # Optional
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """
        String representation of the Transaction object.
        """
        return f"<Transaction {self.title}>"

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """
    Callback function to reload the user object from the user ID stored in the session.
    """
    return User.query.get(int(user_id))
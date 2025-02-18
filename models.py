from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import re
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    @staticmethod
    def validate_name(name):
        if not name or len(name) < 2 or len(name) > 100:
            raise ValueError("Name must be between 2 and 100 characters long.")
        if not name.replace(' ', '').isalpha():
            raise ValueError("Name should only contain letters and spaces.")
        return name

    @classmethod
    def validate_first_name(cls, first_name):
        return cls.validate_name(first_name)

    @classmethod
    def validate_last_name(cls, last_name):
        return cls.validate_name(last_name)

    @staticmethod
    def validate_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")
        return email

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character.")
        return generate_password_hash(password)

    @staticmethod
    def validate_phone(phone):
        phone_regex = r'^\+?1?\d{9,15}$'
        if not re.match(phone_regex, phone):
            raise ValueError("Invalid phone number format.")
        return phone

    @classmethod
    def create_user(cls, first_name, last_name, email, password, phone):
        return cls(
            first_name=cls.validate_first_name(first_name),
            last_name=cls.validate_last_name(last_name),
            email=cls.validate_email(email),
            password=cls.validate_password(password),
            phone=cls.validate_phone(phone)
        )

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)  # Store amount in paise
    shipping_address = db.Column(db.String(255), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)  # Store price in paise
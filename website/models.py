from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class Transactions(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    amt = db.Column(db.Integer)
    t_type = db.Column(db.String(10))
    username = db.Column(db.String(50))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(255))
    username = db.Column(db.String(50), unique=True)
    pin = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    account = db.Column(db.String(10))
    balance = db.Column(db.Float, default=0.0)
    trans = db.relationship('Transactions')

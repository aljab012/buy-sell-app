# models.py

from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True,nullable=False)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000),nullable=False)
    telephone = db.Column(db.Integer,nullable=False)
    def __repr__(self):
        return '<User %r>' % self.name

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(80), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('events', lazy=True))
    details =  db.Column(db.String(80), nullable=False)
    time = db.Column(db.String(80), nullable=False)
    place = db.Column(db.String(80), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('events', lazy=True))
    def __repr__(self):
        return '<Event %r>' % self.name

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    details = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller = db.relationship('User', backref=db.backref('seller', lazy=True))
    pub_date = db.Column(db.String, nullable=False, default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('books', lazy=True))
    def __repr__(self):
        return '<Book %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Category %r>' % self.name
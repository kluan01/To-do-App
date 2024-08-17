from . import db
from flask_login import UserMixin # Custom class that allow usage of Flask login (current_user) through inheritance
from sqlalchemy.sql import func # Allows usage of func for time

# Model = blueprint for data 

class Note(db.Model): 
    id = db.Column(db.Integer, primary_key=True) # ID is auto set
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    due = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Col that always references another Col in a diff database (linkage)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # Primary key to help quickly identify user
    email = db.Column(db.String(150), unique=True) # Unique for duplicates
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # 1 to many relationship w/ Note class

from app import db
from datetime import datetime

class User(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.relationship('Profile', backref='user', uselist=False)

    def __init__(self, email, username, password_hash):
        self.email = email
        self.username = username
        self.password_hash = password_hash

class Profile(db.Model):
    __tablename__= 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    hobbies = db.Column(db.String(255))
    profile_pic = db.Column(db.String(255), default='default.jpg')
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    #field to be added
    visibility = db.Column(db.String(255), default='public')

    
        
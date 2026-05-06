from app import db
from datetime import datetime

class User(db.model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
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

    def __init__(self, email, password, first_name, last_name, age, bio, location, hobbies, visibility):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.bio = bio
        self.location = location
        self.hobbies = hobbies
        self.visibility = visibility
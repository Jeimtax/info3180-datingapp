from app import db
from datetime import datetime

class User(db.Model):
    __tablename__= 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    totp_secret = db.Column(db.String(32), nullable=True)
    totp_enabled = db.Column(db.Boolean, default=False, nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)

    def __init__(self, email, username, password_hash):
        self.email = email
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return '<User %r>' % self.username


class Profile(db.Model):
    __tablename__= 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))

    hobbie1 = db.Column(db.String(255))
    hobbie2 = db.Column(db.String(255))
    hobbie3 = db.Column(db.String(255))

    relationship_goal = db.Column(db.String(100))
    profile_pic = db.Column(db.String(255), default='default.jpg')
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    #field to be added
    visibility = db.Column(db.String(255), default='public')

    def __repr__(self):
        return '<Profile %r %r>' % (self.first_name, self.last_name)
    

class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20)) # like and dislike
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Match %r -> %r: %s>' % (self.user_id, self.target_id, self.status)


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message %r>' % self.id
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True, cascade="all, delete-orphan") # sets up a relationship to todos which references User

    def toDict(self):
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password": self.password
      }
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class UserReact(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    postid = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, primary_key=True)
    react = db.Column(db.String(80), nullable=True)

    def toDict(self):
        return{
            'userid': self.userid,
            'postid': self.postid,
            'react': self.react
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    reacts = db.relationship('UserReact', backref='post', lazy=True, cascade="all, delete-orphan")
    
    def toDict(self):
        return{
            'id': self.id,
            'text': self.text,
            'reacts': self.reacts
        }

    def getTotalLikes(self):
        numLikes = 0
        for react in self.reacts:
            if react.react == 'like':
                numLikes += 1
        return numLikes
    
    def getTotalDislikes(self):
        numDislikes = 0
        for react in self.reacts:
            if react.react == 'dislike':
                numDislikes += 1
        return numDislikes

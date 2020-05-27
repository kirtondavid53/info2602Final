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
    posts = db.relationship('Post', backref='user', lazy=True) # sets up a relationship to todos which references User

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
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    postid = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    react = db.Column(db.String(80), unique=True, nullable=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    reacts = db.relationship('UserReact', backref='post', lazy=True)
    
    def toDict(self):
        return{
            'id': self.id,
            'text': self.text,
            'reacts': self.reacts
        }

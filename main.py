import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, User , Post, UserReact #add application models

''' login form'''
class LogIn(FlaskForm):
  username = StringField('username', validators=[InputRequired()])
  password = PasswordField('New Password', validators=[InputRequired()])
  submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light white-text'})
''' end login form'''


''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

''' End Flask Login Functions '''


def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
#   app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) # uncomment if using flsk jwt
  CORS(app)
  login_manager.init_app(app) # uncomment if using flask login
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

''' Set up JWT here (if using flask JWT)'''
# def authenticate(uname, password):
#   pass

# #Payload is a dictionary which is passed to the function by Flask JWT
# def identity(payload):
#   pass

# jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''

@app.route('/', methods=['GET', 'POST'])
def index():
  form = LogIn()
  if form.validate_on_submit(): # respond to form submission
    data = request.form
    user = User.query.filter_by(username = data['username']).first()
    if user and user.check_password(data['password']): # check credentials
      flash('Logged in successfully.') # send message to next page
      login_user(user) # login the user
      return redirect(url_for('client_app')) # redirect to main page if login successful
    else:
      flash('Invalid username or password') # send message to next page
      return redirect(url_for('index')) # redirect to login page if login unsuccessful
  return render_template('index.html', form=form)

@app.route('/app', methods=['GET'])
@login_required
def client_app():

  posts = Post.query.all()
  results = []
  for post in posts:
    rec = post.toDict() # convert post object to dictionary record
    rec['num_likes'] = post.getTotalLikes # add num likes to dictionary record
    rec['num_dislikes'] = post.getTotalDislikes # add dislikes to dictionary record
    results.append(rec)
  return render_template('app.html', posts=posts, results=results, results=results)


@app.route('/createPost', methods=['POST'])
@login_required
def create_post():
  data = request.form
  post = Post(text=data['text'], userid=current_user.id)
  db.session.add(post)
  db.session.commit()
  flash('Created')
  return redirect(url_for('client_app'))

@app.route('/deletePost/<id>', methods=["GET"])
@login_required
def delete_post(id):
  post = Post.query.filter_by(userid=current_user.id, id=id).first()
  if post == None:
    flash ('Invalid id or unauthorized')
  db.session.delete(post) # delete the object
  db.session.commit()
  flash ('Deleted!')
  return redirect(url_for('client_app'))

@app.route('/updatePost/<id>', methods=['POST'])
@login_required
def update_post(id):
  react = request.form.get('react') # either 'like' or 'dislike'
  print(react)
  oldReact = UserReact.query.filter_by(userid=current_user.id,postid=id).first()
  if oldReact == None:

    userReact = UserReact(react=react, userid=current_user.id,postid=id)
    if userReact == None:
      flash('Invalid id or unauthorized') 
    
    if react == 'like':
      flash('You liked a post')
    elif react == 'dislike':
      flash('You dislikes a post')
    db.session.add(userReact)
    db.session.commit()

  else:
    oldReact.react = react
    flash('You change your react')
    db.session.add(oldReact)
    db.session.commit()

  return redirect(url_for('client_app'))

if __name__ == '__main__':
    app.run(debug=True)

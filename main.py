import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from flask_bootstrap import Bootstrap 

from models import db, User , Post, UserReact #add application models

''' Signup form'''
class SignUp(FlaskForm):
  username = StringField('username', validators=[InputRequired()])
  email = StringField('email', validators=[Email(), InputRequired()])
  password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
  confirm  = PasswordField('Repeat Password')
''' end Signup form'''

''' login form'''
#Login form taken for INFO2602 lab 6
class LogIn(FlaskForm):
  username = StringField('Username', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired()])
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
  Bootstrap(app)
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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignUp() # create form object
  if form.validate_on_submit():
    data = request.form # get data from form submission
    newuser = User(username=data['username'], email=data['email']) # create user object
    newuser.set_password(data['password']) # set password
    db.session.add(newuser) # save new user
    db.session.commit()
    flash('Account Created!')# send message
    return redirect(url_for('index'))# redirect to login page
  return render_template('signup.html', form=form) # pass form object to template

@app.route('/app', methods=['GET'])
@login_required
def client_app():

  posts = Post.query.all()
  results = []
  for post in posts:
    rec = post.toDict() # convert post object to dictionary record
    rec['num_likes'] = post.getTotalLikes() # add num likes to dictionary record
    rec['num_dislikes'] = post.getTotalDislikes() # add dislikes to dictionary record
    results.append(rec)
  return render_template('app.html', posts=posts, results=results)


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
    flash('You changed your react')
    db.session.add(oldReact)
    db.session.commit()

  return redirect(url_for('client_app'))

@app.route('/getreacts',methods=['GET'])
@login_required
def getrecipes():
  posts = UserReact.query.all()
  results = []
  for post in posts:
    rec = post.toDict()
    results.append(rec)
  return json.dumps(results)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

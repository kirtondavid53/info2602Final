from sqlalchemy.exc import IntegrityError
import json
from main import app
from models import db, User

def index():
  bob = User(username="bob", email="bob@mail.com") # creates an object from the User class/model
  bob.set_password("bobpass") # use method to hash password
  try:
    db.session.add(bob)
    db.session.commit() # save user
  except IntegrityError: # attempted to insert a duplicate user
    db.session.rollback()
    return json.dumps({ "error" : "username or email already exists"}) # error message
  return json.dumps({ "message" : "user created"}) # success
 
db.create_all(app=app)
index()
print('database initialized!')
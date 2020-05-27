from sqlalchemy.exc import IntegrityError
import json
from main import app
from models import db, User

def index():
  bob = User(username="bob", email="bob@mail.com") # creates an object from the User class/model
  bob.set_password("bobpass") # use method to hash password
  john = User(username="john", email="john@mail.com")
  john.set_password('johnpass')
  users = [bob.toDict(), john.toDict()]
  try:
    db.session.add(john)
    db.session.add(bob)
    db.session.commit() # save user
  except IntegrityError: # attempted to insert a duplicate user
    db.session.rollback()
    return json.dumps({ "error" : "username or email already exists"}) # error message
  return json.dumps(users) # success
 
db.create_all(app=app)
index()
print('database initialized!')
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email

class LogIn(FlaskForm):
  username = StringField('username', validators=[InputRequired()])
  password = PasswordField('New Password', validators=[InputRequired()])
  submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light white-text'})
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, HiddenField, SubmitField, DateField
from wtforms.validators import DataRequired

class IdeaForm(FlaskForm):
    idea = TextAreaField('idea', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    password = StringField('password', validators = [DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    password = StringField('password', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired()])
    date_of_birth =  DateField('deadline', validators=[DataRequired()])

class PostForm(FlaskForm):
    content = TextAreaField('content', validators = [DataRequired()])
    hashtags = StringField('hashtags', validators=[DataRequired()])




from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, HiddenField, SubmitField, DateField, FileField
from wtforms.validators import DataRequired

class DeletePostForm(FlaskForm):
    post_id = HiddenField('Post ID')
    submit = SubmitField('Delete')

class LoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    password = StringField('password', validators = [DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    password = StringField('password', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired()])
    date_of_birth =  DateField('deadline', validators=[DataRequired()])
    profile_picture = FileField('Profile Picture')
    
class EditProfile(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    password = StringField('password', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired()])
    profile_picture = FileField('Profile Picture')

    
class PostForm(FlaskForm):
    content = TextAreaField('content', validators = [DataRequired()])
    image_or_video = FileField('image')
    hashtags = StringField('hashtags', validators=[DataRequired()])


class EditPost(FlaskForm):
    content = TextAreaField('content', validators = [DataRequired()])
    image_or_video = FileField('image')

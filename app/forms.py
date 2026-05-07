#form classes

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=120)])


class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=100)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=100)])
    age = IntegerField('Age', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    location = StringField('Location', validators=[InputRequired(), Length(max=100)])
    bio = TextAreaField('Bio', validators=[InputRequired()])

    hobbie1 = StringField('Hobbie 1', validators=[InputRequired(), Length(max=255)])
    hobbie2 = StringField('Hobbie 2', validators=[InputRequired(), Length(max=255)])
    hobbie3 = StringField('Hobbie 3', validators=[InputRequired(), Length(max=255)])
    relationship_goal = StringField('Relationship Goal', validators=[InputRequired(), Length(max=100)])

    profile_pic = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    visibility = SelectField('Profile Visibility', choices=[('public', 'Public'), ('private', 'Private')])
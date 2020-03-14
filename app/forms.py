from flask_wtf import FlaskForm
from flask_wtf.file import  FileField, FileRequired, FileAllowed
from wtforms import SelectField,TextAreaField,TextField
from wtforms.validators import InputRequired


class ProfileForm(FlaskForm):
    firstname = TextField('First Name', validators=[InputRequired()])
    lastname = TextField('Last Name', validators=[InputRequired()])
    gender = SelectField('Gender', validators=[InputRequired()],choices = [('male','M'),('female','F')])
    email = TextField('Email', validators=[InputRequired()])
    location = TextField('Location', validators=[InputRequired()])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    profilePicture = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'Images only!'])
    ])

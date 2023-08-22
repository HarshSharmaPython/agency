from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField,RadioField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    firstname=StringField('First Name', validators=[DataRequired()])
    lastname=StringField('Last Name', validators=[DataRequired()])
    email=EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()]) 
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email=EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class req(FlaskForm):
        dic = StringField('discription ', validators=[DataRequired()])
        submit = SubmitField('add')
 
class priceToPlane (FlaskForm):
     plane =SubmitField("purchase")
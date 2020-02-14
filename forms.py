from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import Email, DataRequired

# months = enumerate('January February March April May June July August September October November December'.split(' '))
# days = enumerate(range(1, 32))
# years = [(year, year) for year in range(1970, 2019)]


class SignupForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    name = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from covaid.models import User
from wtforms.widgets import html5


class RegistrationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    street = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email has already been registered with CovAid.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    send = SubmitField('Send')

class RequestForm(FlaskForm):
    item = StringField('Item Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', widget=html5.NumberInput(), validators=[DataRequired()])
    instruct = StringField('Special Instructions')
    send = SubmitField('Place Request')

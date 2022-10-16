from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, Length, EqualTo


csrf = CSRFProtect()


class LogInForm(FlaskForm):
    """Log In Form Format"""
    email = EmailField(validators=[
        Email(
            message="Please include an '@' in the Email Address."),
        DataRequired("Email Address is required."),
    ])
    password = PasswordField(validators=[
        DataRequired("Password is required."),
    ])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    """Register Form Format"""
    email = EmailField(validators=[
        Email(
            message="Please include an '@' in the Email Address."),
        DataRequired("Email Address is required."),
        Length(min=3)
    ])
    password = PasswordField(validators=[
        DataRequired("Password is required."),
        Length(min=4),
        EqualTo('confirmation')
    ])
    confirmation = PasswordField(validators=[
        DataRequired("Confirm Password is required.")
    ])
    submit = SubmitField('Register')


class VerifyOTP(FlaskForm):
    """OTP Form Format for verifying OTP"""
    password = StringField()
    submit = SubmitField('Submit')

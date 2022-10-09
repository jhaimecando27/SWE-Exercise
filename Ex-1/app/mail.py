from flask import session
from flask_mail import Mail, Message

mail = Mail()


def sendOtp(OTP_code):
    """Send OTP to the email in session"""

    msg = Message("Hello", recipients=[session['tmp_email']])
    msg.html = "<p>Your OTP is " + "<b>" + OTP_code + "</b></p>"
    mail.send(msg)

from math import floor
from random import random
from flask import session
from flask_mail import Mail, Message

mail = Mail()


def sendOTP():
    """Send OTP to the email in session"""

    # Generate OTP
    string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    OTP_code = ""
    length = len(string)
    for _ in range(6):
        OTP_code = OTP_code + string[floor(random() * length)]

    print("OTP Code: " + OTP_code)

    # Remember the OTP Code
    session['tmp_OTP'] = OTP_code

    # Send the OTP to the Email address
    msg = Message("Hello", recipients=[session['tmp_email']])
    msg.html = "<p>Your OTP is " + "<b>" + OTP_code + "</b></p>"
    mail.send(msg)

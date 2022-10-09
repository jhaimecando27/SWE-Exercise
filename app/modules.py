from math import floor
from random import random

from flask import session


def getOtp():
    """Generate One Time Password."""
    string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    OTP_code = ""
    length = len(string)
    for _ in range(6):
        OTP_code = OTP_code + string[floor(random() * length)]

    print("OTP Code: " + OTP_code)

    session['tmp_OTP'] = OTP_code
    return OTP_code

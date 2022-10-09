from flask import Blueprint, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .modules import getOtp
from .mail import sendOtp

bp = Blueprint('auth', __name__, url_prefix="/")


@bp.route('/otp', methods=['GET', 'POST'])
def otp():
    """Verify the OTP Authentication"""

    # Ensure user under go login/register route or already logged in
    if session.get("tmp_email") is None or session.get('otp') is True:
        return redirect("/")

    # User submitted a form
    if request.method == 'POST':

        error = None

        # Click the send OTP button
        if request.form.get('sendOTP') == "Send OTP":
            sendOtp(getOtp())
            error = "OTP have been sent to your Email address."

        # Ensure input field is not empty
        elif not request.form.get('otp'):
            error = "Must provide OTP."

        # Ensure otp is valid
        elif request.form.get('otp') != session['tmp_OTP']:
            error = "OTP doesn't matched"

        if error is None:
            db = get_db()

            # If from register route
            if session.get("tmp_pass"):
                db.execute(
                    "INSERT INTO User (email, password) VALUES (?, ?)",
                    (session['tmp_email'], session['tmp_pass'])
                )
                db.commit()

            # Find account
            user = db.execute(
                'SELECT * FROM User WHERE email = ?', (session['tmp_email'],)
            ).fetchone()

            # Forget any User
            session.clear()

            # Remember user
            session['user_id'] = user['id']
            session['otp'] = True

            return redirect('/')

        flash(error)

    # User entered the website
    return render_template('otp.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register the User"""

    # Forget any user
    session.clear()

    # User submitted a form
    if request.method == 'POST':

        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        acc = get_db().execute(
            "SELECT * FROM User where email = ?", (email,)
        ).fetchone()
        error = None

        # Ensure input fields are not empty
        if not email:
            error = "Must provide Email address."
        elif not password:
            error = "Must provide Password."
        elif not confirmation:
            error = "Must provide Confirmation password."

        # Ensure account doesn't exists
        elif acc is not None:
            error = f"Your email {email} already taken."

        # Ensure password and confirmation password matched
        elif password != confirmation:
            error = "Password and Confirmation password doesn't matched."

        if error is None:
            session['tmp_email'] = email
            session['tmp_pass'] = generate_password_hash(password)
            return redirect("/otp")

        flash(error)

    # User entered the website
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Log in the User"""

    # Forget any user
    session.clear()

    # User submitted a form
    if request.method == 'POST':

        email = request.form.get("email")
        password = request.form.get("password")
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        # Ensure input fields are not empty
        if not email:
            error = 'Must provide Email address.'
        elif not password:
            error = 'Must provide Password.'
        # Ensure email exists
        elif user is None:
            error = f"Your email {email} doesn't exsists."

        # Ensure password matched
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # Got to OTP route
        if error is None:
            session['tmp_email'] = email
            return redirect('/otp')

        flash(error)

    # User entered the website
    return render_template('login.html')


@bp.route('/logout')
def logout():
    """Log out the User"""
    session.clear()
    return redirect("/")

from flask import Blueprint, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User, db
from .mail import sendOTP

bp = Blueprint('auth', __name__, url_prefix="/auth")


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
            sendOTP()
            error = "OTP have been sent to your Email address."

        # Ensure input field is not empty
        elif not request.form.get('otp'):
            error = "Must provide OTP."

        # Ensure otp is valid
        elif request.form.get('otp') != session['tmp_OTP']:
            error = "OTP doesn't matched"

        if error is None:

            # If from register route
            if session.get("tmp_pass"):
                user = User(email=session['tmp_email'], password=session['tmp_pass'])
                db.session.add(user)
                db.session.commit()

            # Find account
            user = User.query.filter_by(email=session['tmp_email']).first()

            # Forget any User
            session.clear()

            # Remember user
            print("user.id")
            session['user_id'] = user.id
            session['otp'] = True

            return redirect('/')

        flash(error)

    # User entered the website
    return render_template('/auth/otp.html')


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
        user = User.query.filter_by(email=email).first()
        error = None

        # Ensure input fields are not empty
        if not email:
            error = "Must provide Email address."
        elif not password:
            error = "Must provide Password."
        elif not confirmation:
            error = "Must provide Confirmation password."

        # Ensure account doesn't exists
        elif user:
            error = f"Your email {email} already taken."

        # Ensure password and confirmation password matched
        elif password != confirmation:
            error = "Password and Confirmation password doesn't matched."

        if error is None:
            session['tmp_email'] = email
            session['tmp_pass'] = generate_password_hash(password)
            return redirect("/auth/otp")

        flash(error)

    # User entered the website
    return render_template('/auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Log in the User"""

    # Forget any user
    session.clear()

    # User submitted a form
    if request.method == 'POST':

        email = request.form.get("email")
        password = request.form.get("password")
        error = None
        user = User.query.filter_by(email=email).first()

        # Ensure input fields are not empty
        if not email:
            error = 'Must provide Email address.'
        elif not password:
            error = 'Must provide Password.'
        # Ensure email exists
        elif user is None:
            error = f"Your email {email} doesn't exsists."

        # Ensure password matched
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        # Got to OTP route
        if error is None:
            session['tmp_email'] = email
            return redirect('/auth/otp')

        flash(error)

    # User entered the website
    return render_template('/auth/login.html')


@bp.route('/logout')
def logout():
    """Log out the User"""
    session.clear()
    return redirect("/")

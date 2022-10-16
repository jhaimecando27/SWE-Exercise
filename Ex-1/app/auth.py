from flask import Blueprint, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from app.forms import LogInForm, RegisterForm, VerifyOTP
from app.models import User, db
from .mail import sendOTPMail

bp = Blueprint('auth', __name__, url_prefix="/auth")


@bp.route('/otp', methods=['GET', 'POST'])
def otp():
    """Verify the OTP Authentication"""

    # Ensure user under go login/register route or already logged in
    if session.get("tmp_email") is None or session.get('otp') is True:
        return redirect("/")

    form = VerifyOTP()

    if request.method == 'POST':

        error = None

        # User wants OTP to be send to email
        if request.form.get('sendOTP') == "Send OTP":
            sendOTPMail()
            error = "OTP have been sent to your Email address."

        # User verifies OTP
        elif form.validate_on_submit():

            # Ensure otp is valid
            if form.password.data != session['tmp_OTP']:
                error = "OTP doesn't matched"

            if error is None:

                # If from register route
                if session.get("tmp_pass"):
                    user = User(email=session['tmp_email'],
                                password=session['tmp_pass'])
                    db.session.add(user)
                    db.session.commit()

                # Find account
                user = User.query.filter_by(
                    email=session['tmp_email']).first()

                # Cleans up the 'tmp_email', 'tmp_pass', 'tmp_OTP'
                session.clear()

                # Remember user
                print("user.id")
                session['user_id'] = user.id
                session['otp'] = True

                return redirect('/')

        flash(error)

    # User entered the website
    return render_template('/auth/otp.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register the User"""

    # Forget any user
    session.clear()
    form = RegisterForm()

    # User submitted a form
    if request.method == 'POST':
        print("test")

        if form.validate_on_submit():

            # User inputs
            email = form.email.data
            password = form.password.data

            # Query the input email
            user = User.query.filter_by(email=email).first()

            error = None

            # Ensure account doesn't exists
            if user:
                error = f"Your email {email} already taken."

            if error is None:
                session['tmp_email'] = email
                session['tmp_pass'] = generate_password_hash(password)
                return redirect("/auth/otp")

            flash(error)
        print(form.errors)

    # User entered the website
    return render_template('/auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Log in the User"""

    # Forget any user
    session.clear()

    form = LogInForm()

    # User submitted a form
    if request.method == 'POST' and form.validate_on_submit():

        # User inputs
        email = form.email.data
        password = form.password.data

        error = None

        # Query the input email
        user = User.query.filter_by(email=email).first()

        # Ensure email exists
        if user is None:
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
    return render_template('/auth/login.html', form=form)


@bp.route('/logout')
def logout():
    """Log out the User"""
    session.clear()
    return redirect("/")

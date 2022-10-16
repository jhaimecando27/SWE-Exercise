from flask import Blueprint, render_template, session

from app.models import User

bp = Blueprint('views', __name__, url_prefix="/")


@bp.route('/')
def index():
    """Home Page"""

    user = "Hello"

    if session.get('user_id') is not None:
        user = User.query.filter_by(id=session['user_id']).first()
        user = user.email

    if user == "Hello":
        session.clear()

    return render_template('index.html', user=user)

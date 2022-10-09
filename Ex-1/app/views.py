from flask import Blueprint, render_template, session

from .db import get_db

bp = Blueprint('views', __name__, url_prefix="/")


@bp.route('/')
def index():
    """Home Page"""

    user = "Hello"

    if session.get('user_id') is not None:
        db = get_db()
        user = db.execute(
            'SELECT email FROM User WHERE id = ?', (session['user_id'],)
        ).fetchone()
        user = user['email']

    return render_template('index.html', user=user)

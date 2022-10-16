from os import makedirs
from flask import Flask

from .mail import mail


def create_app():
    """Create application"""

    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')

    # Ensure the instance folder exists
    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth, views
    from app.models import db

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    app.add_url_rule('/', endpoint='index')

    return app

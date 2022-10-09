from os import path, makedirs
from flask import Flask

from .mail import mail


def create_app():
    """Create application"""

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=path.join(app.instance_path, 'database.sqlite')
    )
    app.config.from_object('config.DevConfig')

    # Ensure the instance folder exists
    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    from . import db, auth, views

    db.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    app.add_url_rule('/', endpoint='index')

    return app

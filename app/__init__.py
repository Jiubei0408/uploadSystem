import os

from flask_login import LoginManager
from flask import Flask

from app.models.base import db

login_manager = LoginManager()


def register_bp(flask_app):
    from app.routers import get_blueprints
    for bp in get_blueprints():
        bp_name, url_prefix = bp
        flask_app.register_blueprint(bp_name, url_prefix=url_prefix)


def register_plugin(flask_app):
    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

    login_manager.init_app(flask_app)


def create_app(name):
    flask_app = Flask(name)

    flask_app.config.from_object('app.config.secure')
    upload_path = os.path.join(flask_app.root_path, 'uploads')
    flask_app.config['UPLOAD_PATH'] = upload_path
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    register_plugin(flask_app)
    register_bp(flask_app)

    return flask_app

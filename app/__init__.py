import os
from datetime import date, datetime

from flask_login import LoginManager
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from flask_bootstrap import Bootstrap

from app.models.base import db
from app.libs.error_code import ServerError


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder


login_manager = LoginManager()
bootstrap = Bootstrap()


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
    bootstrap.init_app(flask_app)


def create_app(name):
    flask_app = Flask(name)

    flask_app.config.from_object('app.config.secure')
    upload_path = os.path.join(flask_app.root_path, 'uploads')
    flask_app.config['UPLOAD_PATH'] = upload_path
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    register_bp(flask_app)
    register_plugin(flask_app)

    return flask_app

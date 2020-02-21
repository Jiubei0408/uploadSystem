import os

from app.models.base import db
from flask import Flask
from app.routers import get_blueprints


def create_app(name):
    flask_app = Flask(name)
    flask_app.config.from_object('app.config.secure')
    flask_app.config['UPLOAD_PATH'] = os.path.join(flask_app.root_path, 'uploads')

    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

    for bp in get_blueprints():
        flask_app.register_blueprint(bp)

    return flask_app

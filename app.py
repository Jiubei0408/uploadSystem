from flask_bootstrap import Bootstrap

from app import create_app

app = create_app(__name__)

bootstrap = Bootstrap(app)

if __name__ == '__main__':
    app.run(port=80)


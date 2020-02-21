from app.routers import (main, session)


def get_blueprints():
    return [(main.bp, '/'),
            (session.bp, '/session')]

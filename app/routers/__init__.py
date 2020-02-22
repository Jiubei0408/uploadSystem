from app.routers import (main, session, notifications)


def get_blueprints():
    return [(main.bp, '/'),
            (session.bp, '/session'),
            (notifications.bp, '/notifications')]

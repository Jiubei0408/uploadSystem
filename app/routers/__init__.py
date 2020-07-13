from app.routers import main, notifications, session


def get_blueprints():
    return [(main.bp, '/'),
            (session.bp, '/session'),
            (notifications.bp, '/notification')]

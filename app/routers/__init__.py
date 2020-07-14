from app.routers import notifications, session


def get_blueprints():
    return [(session.bp, '/session'),
            (notifications.bp, '/notification')]

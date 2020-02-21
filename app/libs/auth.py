import functools

from flask_login import current_user


def admin_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.permission != 1:
            return "你没有相应的权限", 403
        return func(*args, **kwargs)

    return wrapper

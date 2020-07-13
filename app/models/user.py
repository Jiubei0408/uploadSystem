from flask_login import UserMixin
from sqlalchemy import Column, DateTime, Integer, String

from app import login_manager
from app.libs.error_code import AuthFailed
from app.models.base import Base


class User(UserMixin, Base):
    __tablename__ = 'user'

    @property
    def id(self):
        return self.username

    username = Column(String(100), primary_key=True)
    password = Column(String(100))
    nickname = Column(String(100))
    permission = Column(Integer, default=0)
    update_time = Column(DateTime)

    @staticmethod
    @login_manager.user_loader
    def load_user(id_):
        return User.get_by_id(id_)

    @staticmethod
    @login_manager.unauthorized_handler
    def unauthorized_handler():
        raise AuthFailed()

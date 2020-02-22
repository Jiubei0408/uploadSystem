from sqlalchemy import Column, DateTime, String, Integer
from flask_login import UserMixin

from app.models.base import Base
from app import login_manager

from app.libs.error_code import AuthFailed


class User(UserMixin, Base):
    __tablename__ = 'user'

    @property
    def id(self):
        return self.userId

    @property
    def name(self):
        return self.userName

    userId = Column(Integer, primary_key=True, autoincrement=True)
    # 登录名，学生（用户）可以是学号，教师可以是工号，甚至本名也行
    userName = Column(String(100))
    password = Column(String(100), default=123456, nullable=False)
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

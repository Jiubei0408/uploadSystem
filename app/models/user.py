from sqlalchemy import Column, DateTime, String, Boolean
from flask_login import UserMixin

from app.models.base import Base
from app import login_manager


class User(UserMixin, Base):
    __tablename__ = 'user'

    @property
    def id(self):
        return self.studentId

    studentId = Column(String(100), primary_key=True)
    password = Column(String(100))
    nickname = Column(String(100))
    remember_me = Column(Boolean, default=False)
    update_time = Column(DateTime)

    @staticmethod
    @login_manager.user_loader
    def load_user(id_):
        return User.get_by_id(id_)
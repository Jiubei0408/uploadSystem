from sqlalchemy import Column, ForeignKey, Integer, String

from .base import Base
from .user import User


class Notifications(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    detail = Column(String(10000))
    confirm_count = Column(Integer, default=0)
    total = Column(Integer)
    creator = Column(String(100), ForeignKey(User.username))

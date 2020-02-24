from sqlalchemy import Column, Integer, String, ForeignKey

from .base import Base
from .user import User


class Notifications(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(10000))
    checked = Column(Integer, default=0)
    total = Column(Integer)
    username = Column(String(100), ForeignKey(User.username))

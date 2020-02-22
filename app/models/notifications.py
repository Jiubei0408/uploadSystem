from sqlalchemy import Column, Integer, String

from .base import Base


class Notifications(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(10000))
    checked = Column(Integer, default=0)

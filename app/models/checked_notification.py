from sqlalchemy import Column, Integer, String, ForeignKey

from .base import Base
from .user import User
from .notifications import Notifications


class CheckedNotification(Base):
    __tablename__ = 'checked_notification'
    fields = ['nf_id', 'user_id']

    nf_id = Column(Integer, ForeignKey(Notifications.id), primary_key=True)
    user_id = Column(String(100), ForeignKey(User.username), primary_key=True)

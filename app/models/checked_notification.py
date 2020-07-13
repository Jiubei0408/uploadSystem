from sqlalchemy import Column, ForeignKey, Integer, String

from .base import Base
from .notifications import Notifications
from .user import User


class CheckedNotification(Base):
    __tablename__ = 'checked_notification'
    fields = ['nf_id', 'user_id']

    nf_id = Column(Integer, ForeignKey(Notifications.id), primary_key=True)
    user_id = Column(String(100), ForeignKey(User.username), primary_key=True)

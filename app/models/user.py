from app.models.base import Base
from sqlalchemy import Column, Integer, DateTime, String


class User(Base):
    __tablename__ = 'user'
    studentId = Column(Integer, primary_key=True)
    name = Column(String(100))
    isolution = Column(Integer)
    code_color = Column(Integer)
    submit_time = Column(DateTime)
    times = Column(Integer)

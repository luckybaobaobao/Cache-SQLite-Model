from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Joke(Base):
    __tablename__ = 'joke'

    id = Column(Integer, primary_key=True)
    external_id = Column(String(50), unique=True)
    value = Column(Text)
    url = Column(String(100), nullable=True)
    icon_url = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

    def __repr__(self):
        return self.id

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
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

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)


class JokeCategoryRelation(Base):
    __tablename__ = 'relation'

    id = Column(Integer, primary_key=True)
    joke_id = Column(Integer, ForeignKey('joke.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

class DeletedRemoteJoke(Base):
    __tablename__ = 'deleted'

    id = Column(Integer, primary_key=True)
    external_id = Column(String(50), unique=True)

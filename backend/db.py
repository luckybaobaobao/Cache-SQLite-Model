from sqlalchemy import create_engine
from models import Base
from sqlalchemy.orm import sessionmaker

Database = "jokes"
engine = create_engine(f'sqlite:///{Database}', echo=True)


def create_tables():
    Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

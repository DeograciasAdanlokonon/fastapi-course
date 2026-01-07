from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# password = 'Testme%4013467'
# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{password}@localhost/TodoAppDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

class Base(DeclarativeBase):
    pass
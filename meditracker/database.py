from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///medi_tracker.db"

engine = create_engine(
    DATABASE_URL,
    echo = True
)

class Base(DeclarativeBase):
    pass

Session = sessionmaker(
    bind = engine
)
import sqlalchemy as db
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

# engine = db.create_engine("sqlite+pysqlite:///:memory:", echo = True)

engine = db.create_engine("postgresql://postgres@localhost/db_hw2", echo=True)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


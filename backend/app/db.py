from os import environ
from _collections_abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase , Session, sessionmaker


class Base(DeclarativeBase):
    pass


def make_engine():
    return create_engine(environ["DATABASE_URL"], pool_pre_ping=True)

SessionLocal= sessionmaker(autocommit=False,autoflush=False)

def get_db() -> Generator[Session, None,None]:
    engine = make_engine()
    with SessionLocal(bind=engine) as session:
        yield session
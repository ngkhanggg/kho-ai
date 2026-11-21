from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def make_engine():
    return create_engine(environ["DATABASE_URL"])

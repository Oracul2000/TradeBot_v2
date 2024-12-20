from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.user import *
from models.base import *


def init_db():
    engine = create_engine("sqlite:///Data.db")
    Base.metadata.create_all(engine)


init_db()
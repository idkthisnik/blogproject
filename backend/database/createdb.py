import os
import sys

sys.path.insert(0, os.getcwd())

from database.models import *
from database.connection import engine, Base
from sqlalchemy import MetaData

metadata = MetaData()

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
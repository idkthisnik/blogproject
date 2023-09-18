import sys
sys.path.insert(0, "D:\projects\\blog")

from backend.database.models import *
from backend.database.connection import engine
from sqlalchemy import MetaData

metadata = MetaData()

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
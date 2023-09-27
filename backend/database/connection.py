import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

server = os.environ['DATABASE_SERVER']
database = os.environ['DATABASE_NAME']
username = os.environ['DATABASE_LOGIN']
password = os.environ['DATABASE_PASSWORD']
port = os.environ['DATABASE_PORT']

sql_alchemy_url = f"mssql://{username}:{password}@{server}:{port}/{database}?driver=FreeTDS"

engine = create_engine(sql_alchemy_url, echo=False)

Base = declarative_base()
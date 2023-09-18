from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from backend.config import DATABASE_LOGIN, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME

sql_alchemy_url = f'mssql+pyodbc://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server'

engine = create_engine(sql_alchemy_url, echo=False)

Base = declarative_base()
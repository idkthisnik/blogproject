import os
from dotenv import load_dotenv

config = load_dotenv('backend\.env')


DATABASE_LOGIN = os.getenv('DATABASE_LOGIN')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')

FASTAPI_DOMAIN=os.getenv('FASTAPI_DOMAIN')
FASTAPI_HOST=os.getenv('FASTAPI_HOST')
FASTAPI_PORT=os.getenv('FASTAPI_PORT')

REACT_DOMAIN=os.getenv('REACT_DOMAIN')

JWT_SECRET=os.getenv('JWT_SECRET')
JWT_ALGORITHM=os.getenv('JWT_ALGORITHM')

PEPPER=os.getenv('PEPPER')
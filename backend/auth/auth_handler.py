import time
from starlette.responses import JSONResponse
from backend.config import JWT_ALGORITHM, JWT_SECRET
import jwt

from backend.database.crud.user_crud import UserCrud

user_crud = UserCrud()


def token_response(token: str):
    return {
        "access_token": token
    }
    
    
def signJWT(userId: str, expire: int) -> JSONResponse:
    
    payload = {
        "userId": userId,
        "expires": time.time() + expire
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
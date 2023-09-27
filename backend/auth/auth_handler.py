import os
import jwt
import time
from starlette.responses import JSONResponse

from database.crud.user_crud import UserCrud

user_crud = UserCrud()


def token_response(token: str) -> dict:
    return {
        "access_token": token
    }
        
def signJWT(userId: str, expire: int) -> JSONResponse:
    
    payload = {
        "userId": userId,
        "expires": time.time() + expire
    }
    token = jwt.encode(
        payload,
        os.environ['JWT_SECRET'],
        algorithm=os.environ['JWT_ALGORITHM']
    )
    return token

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token,
            os.environ['JWT_SECRET'],
            algorithms=os.environ['JWT_ALGORITHM']
        )
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
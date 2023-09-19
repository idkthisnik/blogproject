import sys
import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination.utils import disable_installed_extensions_check


sys.path.insert(0, "D:\projects\\blog")

from backend.config import FASTAPI_DOMAIN, FASTAPI_HOST, FASTAPI_PORT, REACT_DOMAIN
from auth_routers import router as auth_router
from post_routers import router as post_router
from comment_routers import router as comment_router
from subscription_routers import router as subscriptions_router
from user_routers import router as user_router
from settings_routers import router as settings_router

#disable fastapi_pagination console messages 
disable_installed_extensions_check()

app = FastAPI(title='Blog')

add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[REACT_DOMAIN, FASTAPI_DOMAIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = (auth_router, post_router,
           comment_router, subscriptions_router,
           user_router, settings_router
            )

for r in routers:
    app.include_router(r)
    

if __name__ == "__main__":
    uvicorn.run(app, host=FASTAPI_HOST, port=int(FASTAPI_PORT))
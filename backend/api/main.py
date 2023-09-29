import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination.utils import disable_installed_extensions_check


sys.path.insert(0, os.getcwd())


from api.auth_routers import router as auth_router
from api.post_routers import router as post_router
from api.comment_routers import router as comment_router
from api.subscription_routers import router as subscriptions_router
from api.user_routers import router as user_router
from api.settings_routers import router as settings_router

#disable fastapi_pagination console messages 
disable_installed_extensions_check()

app = FastAPI(title='Blog')

app.mount("/static", StaticFiles(directory="static"), name="static")

add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.environ['REACT_DOMAIN'],
        os.environ['FASTAPI_DOMAIN'],
        os.environ['REACT_LOCALHOST_DOMAIN']
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = (
    auth_router, post_router,
    comment_router, subscriptions_router,
    user_router, settings_router
)

for r in routers:
    app.include_router(r)
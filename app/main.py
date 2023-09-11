from fastapi import FastAPI
from app.routers.user import router as router_user
from app.routers.auth import router as router_auth

app = FastAPI()

app.include_router(router_user)
app.include_router(router_auth)
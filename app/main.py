from fastapi import FastAPI
from app.routers.user import router as router_user

app = FastAPI()

@app.get('/')
def root():
    return 'It\'s working!'


app.include_router(router_user)
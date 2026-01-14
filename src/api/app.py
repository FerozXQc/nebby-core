from fastapi import FastAPI
from src.api.routers import auth_router
app = FastAPI()
app.include_router(auth_router, prefix='/auth',tags=['auth'])
@app.get('/')
def health_check():
    return 'hello world'
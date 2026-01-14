from fastapi import FastAPI
from src.api.routers import auth_router, template_router

app = FastAPI()
app.include_router(auth_router, prefix='/auth',tags=['auth'])
app.include_router(template_router, prefix='/template',tags=['template'])

@app.get('/')
def health_check():
    return 'hello world'
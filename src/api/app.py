from fastapi import FastAPI
from src.api.auth.auth_router import router as auth_router
from src.api.onboarding.onboarding_router import router as ob_router 
app = FastAPI()
app.include_router(auth_router,prefix-'/auth',tags=['auth'])
app.include_router(ob_router,prefix='/onboarding',tags=['onboarding'])
@app.get('/')
def health_check():
    return 'hello world'
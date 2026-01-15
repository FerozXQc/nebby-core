from fastapi import APIRouter, Depends, HTTPException, Request, Response
from datetime import timedelta
from jose import JWTError, jwt
import os

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from uuid import UUID
from src.db.schemas.auth_schema import registerUserSchema, loginUserSchema
from src.db.dependencies import get_db
from src.db.services.auth_service import AuthService
from src.utils.password import verify_hashed_password

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login",auto_error=False)

def get_auth_service(session: Session = Depends(get_db)) -> AuthService:
    return AuthService(session)

async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),  # OAuth2 (header)
    auth_service: AuthService = Depends(get_auth_service)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    jwt_token = request.cookies.get("access_token") or token
    if not jwt_token:
        raise credentials_exception
    try:
        payload = jwt.decode(
            jwt_token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")])
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = auth_service.fetch_user_by_id(UUID(user_id))
    if not user:
        raise credentials_exception
    return user

@router.post("/register")
def register_user(
    register_schema: registerUserSchema,
    auth_service: AuthService = Depends(get_auth_service)):
    if auth_service.fetch_user_by_email(register_schema.email):
        raise HTTPException(409, detail="Email already exists")

    user = auth_service.register_user(register_schema)
    if not user:
        raise HTTPException(500, detail="User creation failed")
    print(user)
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
    }

@router.post("/login")
def login_user(
    login_schema: loginUserSchema,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),):
    user = auth_service.fetch_user_by_email(login_schema.email)
    if not user:
        raise HTTPException(404, detail="User not found")

    if not verify_hashed_password(login_schema.password, user.hashed_password):
        raise HTTPException(401, detail="Invalid credentials")

    access_token = auth_service.create_access_token(
        user_id=str(user.id),
        email=user.email,
        expires_delta=timedelta(minutes=15),
    )

    refresh_token = auth_service.create_refresh_token(
        user_id=str(user.id),
        email=user.email,
        expires_delta=timedelta(days=7),
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # True in prod
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return {
        "access_token": access_token,  # 👈 OAuth2 clients
        "token_type": "bearer",
    }

@router.post("/refresh")
def refresh_access_token(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(401, detail="Invalid refresh token")

    try:
        payload = jwt.decode(
            refresh_token,
            os.getenv("REFRESH_TOKEN_SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")],
        )

        user_id = payload.get("sub")
        email = payload.get("email")
        if not user_id or not email:
            raise HTTPException(401)

    except JWTError:
        raise HTTPException(401)

    new_access_token = auth_service.create_access_token(
        user_id=user_id,
        email=email,
        expires_delta=timedelta(minutes=15),
    )

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return {"message": "Access token refreshed"}

@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
    }

@router.get("/logout")
def logout(response: Response,current_user=Depends(get_current_user)):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}

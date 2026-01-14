from datetime import datetime, timedelta, timezone
from jose import jwt
import os
import uuid

from sqlalchemy.orm import Session
from src.db.repositories.auth_repository import AuthRepository
from src.db.schemas.auth_schema import registerUserSchema


class AuthService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = AuthRepository(self.session)

    def register_user(self, register_schema: registerUserSchema):
        return self.repository.create_user(register_schema)

    def fetch_user_by_email(self, email: str):
        return self.repository.fetch_user_by_email(email)

    def fetch_user_by_id(self, user_id: uuid.UUID):
        return self.repository.fetch_user_by_id(user_id)

    def create_access_token(
        self,
        *,
        user_id: str,
        email: str,
        expires_delta: timedelta,
    ) -> str:
        payload = {
            "sub": user_id,      # OAuth2 standard
            "email": email,
            "exp": datetime.now(timezone.utc) + expires_delta,
        }
        return jwt.encode(
            payload,
            os.getenv("SECRET_KEY"),
            algorithm=os.getenv("ALGORITHM"),
        )

    def create_refresh_token(
        self,
        *,
        user_id: str,
        email: str,
        expires_delta: timedelta,
    ) -> str:
        payload = {
            "sub": user_id,
            "email": email,
            "exp": datetime.now(timezone.utc) + expires_delta,
        }
        return jwt.encode(
            payload,
            os.getenv("REFRESH_TOKEN_SECRET_KEY"),
            algorithm=os.getenv("ALGORITHM"),
        )

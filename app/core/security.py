from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings
from app.schema.user import UserLoginOut

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def _create_token(data: dict, expires_delta: timedelta) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    payload["exp"] = expire
    return jwt.encode(
        payload,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm
    )

def create_access_token(user_id: str) -> str:
    return _create_token(
        {"sub": user_id, "typ": "access"},
        timedelta(minutes=settings.jwt.access_expire_min)
    )

def create_refresh_token(user_id: str) -> str:
    return _create_token(
        {"sub": user_id, "typ": "refresh"},
        timedelta(days=settings.jwt.refresh_expire_days)
    )


def create_token_pair(user_id: str) -> UserLoginOut:
    return UserLoginOut(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
        token_type="bearer"
    )

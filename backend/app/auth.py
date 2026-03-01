from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.settings import auth


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=auth.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, auth.secret_key, algorithm=auth.algorithm)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, auth.secret_key, algorithms=[auth.algorithm])
    except JWTError:
        return None

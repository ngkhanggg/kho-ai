import uuid
from datetime import datetime, timedelta, timezone
from os import environ
from typing import Any

import jwt
from pwdlib import PasswordHash

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

def hash_password(plain_password:str) -> str:
    return password_hash.hash(plain_password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(user_id:str, shop_id:str, email:str) -> tuple[str,str,int]:
    now = datetime.now(timezone.utc)
    lifetime = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = now + lifetime
    jti = str(uuid.uuid4())

    payload: dict[str, Any] = {
        "email": email,
        "shop_id": shop_id,
        "sub": user_id,
        "iat": now,
        "exp": expire,
        "jti": jti,
    }
    token = jwt.encode(
        payload, environ["JWT_SECRET_KEY"], algorithm=JWT_ALGORITHM
    )
    return token, jti, int(lifetime.total_seconds())

def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        environ["JWT_SECRET_KEY"],
        algorithms=[JWT_ALGORITHM],
        options={"require": ["sub", "iat", "exp", "jti"]},
    )


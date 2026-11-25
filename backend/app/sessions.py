from datetime import datetime, timezone
from functools import lru_cache
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyCookie, HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from pydantic import AwareDatetime, BaseModel, ValidationError
from sqlalchemy import Engine, delete, select
from sqlalchemy.dialects.postgresql import insert

from app.db import make_engine
from app.models import RevokedAccessToken
from app.security import decode_access_token


class AccessSession(BaseModel):
    sub: UUID
    shop_id: UUID
    email: str
    jti: UUID
    exp: AwareDatetime


SESSION_COOKIE_NAME = "khoai_session"
SESSION_COOKIE_PATH = "/api"
SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

cookie_scheme = APIKeyCookie(name=SESSION_COOKIE_NAME, auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)


def require_same_origin(request: Request) -> None:
    expected_origin = f"{request.url.scheme}://{request.url.netloc}"
    if request.headers.get("origin") != expected_origin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="A same-origin request is required.",
        )


def use_secure_cookie(request: Request) -> bool:
    local_http = (
        request.url.scheme == "http"
        and request.url.hostname in {"localhost", "127.0.0.1", "::1"}
    )
    return not local_http


def invalid_session() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired session.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_signed_session(
    request: Request,
    cookie: Annotated[str | None, Depends(cookie_scheme)],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> AccessSession:
    if cookie is not None:
        if request.method not in SAFE_METHODS:
            require_same_origin(request)
        token = cookie
    elif credentials is not None:
        token = credentials.credentials
    else:
        raise invalid_session()
    try:
        return AccessSession.model_validate(decode_access_token(token))
    except (InvalidTokenError, ValidationError) as exc:
        raise invalid_session() from exc


@lru_cache(maxsize=1)
def get_session_engine() -> Engine:
    return make_engine()


def require_active_session(
    session: Annotated[AccessSession, Depends(get_signed_session)],
    engine: Annotated[Engine, Depends(get_session_engine)],
) -> AccessSession:
    with engine.connect() as connection:
        revoked = connection.scalar(
            select(RevokedAccessToken.jti).where(RevokedAccessToken.jti == session.jti)
        )
    if revoked is not None or session.exp <= datetime.now(timezone.utc):
        raise invalid_session()
    return session


def revoke_session(engine: Engine, session: AccessSession) -> None:
    with engine.begin() as connection:
        connection.execute(
            delete(RevokedAccessToken).where(
                RevokedAccessToken.expires_at <= datetime.now(timezone.utc)
            )
        )
        connection.execute(
            insert(RevokedAccessToken)
            .values(jti=session.jti, expires_at=session.exp)
            .on_conflict_do_nothing(index_elements=[RevokedAccessToken.jti])
        )

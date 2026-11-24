from datetime import datetime, timezone
from functools import lru_cache
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
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


bearer_scheme = HTTPBearer(auto_error=False)


def invalid_session() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired session.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_signed_session(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> AccessSession:
    if credentials is None:
        raise invalid_session()
    try:
        return AccessSession.model_validate(decode_access_token(credentials.credentials))
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

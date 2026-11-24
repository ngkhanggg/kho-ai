from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.ports import InMemoryUserRepository, UserRepositoryProtocol
from app.schema import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from app.security import create_access_token, hash_password, verify_password
from sqlalchemy.orm import Session
from app.db import get_db
from app.repository import PostgreUserRepository

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
_default_repo= InMemoryUserRepository()

def get_user_repo(db: Annotated[Session, Depends(get_db)]) -> UserRepositoryProtocol:
    return PostgreUserRepository(db)

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    body:RegisterRequest,
    repo: Annotated[UserRepositoryProtocol, Depends(get_user_repo)]
):
    if repo.get_by_email(body.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )
    try:
        created = repo.create_user_with_shop(
            full_name=body.full_name,
            shop_name=body.shop_name,
            email=body.email,
            password_hash=hash_password(body.password),
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )
    return RegisterResponse(
        user_id=created.user_id,
        shop_id=created.shop_id,
        full_name=created.full_name,
        email=created.email,
        created_at=created.created_at,
    )

@router.post("/login", response_model=LoginResponse)
def login(
    body: LoginRequest,
    repo: Annotated[UserRepositoryProtocol, Depends(get_user_repo)],
) -> LoginResponse:
    user = repo.get_by_email(body.email)

    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token, _, expires_in = create_access_token(
        user_id=str(user.user_id),
        shop_id=str(user.shop_id),
        email=user.email,
    )
    return LoginResponse(
        access_token=token,
        expires_in=expires_in,
    )

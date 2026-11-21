from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.ports import InMemoryUserRepository, UserRepositoryProtocol
from app.schema import RegisterRequest, RegisterResponse
from app.security import hash_password

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
_default_repo= InMemoryUserRepository()

def get_user_repo() -> UserRepositoryProtocol:
    return _default_repo

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
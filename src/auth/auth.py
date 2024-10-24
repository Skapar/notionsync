from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from ..app.db import get_async_db
from .models import User

from .dependencies import get_current_user
from .schemas import Token
from .utils import (
    create_access_token,
    get_password_hash,
    verify_password,
    decode_refresh_token,
    create_refresh_token,
)

from ..app.config import settings

router = APIRouter()

router.include_router(
    router,
    prefix=settings.api.v1.auth,
)


class UserCredentials(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_async_db),
):
    query = select(User).where(User.username == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})

    refresh_token = create_refresh_token(data={"sub": user.username})

    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/register", response_model=TokenResponse)
async def register_user(
    credentials: UserCredentials = Body(...), db: Session = Depends(get_async_db)
):
    query = select(User).where(User.username == credentials.username)
    result = await db.execute(query)
    user = result.scalars().first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = get_password_hash(credentials.password)
    new_user = User(username=credentials.username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()

    access_token = create_access_token(data={"sub": new_user.username})
    refresh_token = create_refresh_token(data={"sub": new_user.username})

    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh-token", response_model=Token)
def get_access_token(
    refresh_token: str = Body(...), db: Session = Depends(get_async_db)
):
    username = decode_refresh_token(refresh_token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    query = select(User).where(User.username == username)
    result = db.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

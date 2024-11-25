from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.auth import create_access_token
from src.db import get_async_db_session
from src.auth.managers.manager import create_user, confirm_user_phone, authenticate_user, reset_user_password, \
    generate_password_reset_token
from src.auth.models import User

from src.auth.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_user(name: str, phone: str, password: str, db: AsyncSession = Depends(get_async_db_session)):
    await create_user(db, name, phone, password)
    return {"message": "User registered successfully, confirmation code sent"}


# @router.post("/confirm")
# async def confirm_phone(phone: str, code: str, db: AsyncSession = Depends(get_async_db_session)):
#     await confirm_user_phone(db, phone, code)
#     return {"message": "Phone number confirmed"}


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: AsyncSession = Depends(get_async_db_session)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect phone or password")
    if not user.is_phone_confirmed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Phone number not confirmed")

    access_token = create_access_token(data={'sub': str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/reset-password")
# async def reset_password(phone: str, db: AsyncSession = Depends(get_async_db_session),
#                          user: User = Depends(get_current_user)):
#     await generate_password_reset_token(db, phone, user)
#     return {"message": "Password reset code sent"}


# @router.post("/confirm-reset")
# async def confirm_reset_password(phone: str, code: str, new_password: str,
#                                  db: AsyncSession = Depends(get_async_db_session)):
#     await reset_user_password(db, phone, code, new_password)
#     return {"message": "Password updated successfully"}

# @router.post("/change-password")
# async def change_password(new_password: str, current_user: User = Depends(get_current_user),
#                           db: AsyncSession = Depends(get_async_db_session)):
#     await change_user_password(db, current_user, new_password)
#     return {"message": "Password changed successfully"}

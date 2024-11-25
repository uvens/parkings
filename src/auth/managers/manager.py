from sqlalchemy.ext.asyncio import AsyncSession
from random import randint
from sqlalchemy import select
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
from src.auth.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Логика для отправки SMS (заглушка)
def send_sms(phone: str, message: str):
    print(f"Sending SMS to {phone}: {message}")


async def create_user(db: AsyncSession, name: str, phone: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    new_user = User(name=name, number=phone, password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    confirmation_code = str(randint(100000, 999999))
    new_user.phone_confirmation_code = confirmation_code
    send_sms(phone, f"Your confirmation code: {confirmation_code}")

    await db.commit()
    return new_user


async def confirm_user_phone(db: AsyncSession, phone: str, code: str) -> None:
    snmt = select(User).filter(User.number == phone)
    user_query = await db.execute(snmt)
    user = user_query.scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.phone_confirmation_code != code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid confirmation code")

    user.is_phone_confirmed = True
    user.phone_confirmation_code = None
    await db.commit()


async def authenticate_user(db: AsyncSession, phone: str, password: str) -> User:
    snmt = select(User).filter(User.number == phone)
    user_query = await db.execute(snmt)
    user = user_query.scalar()
    if not user or not verify_password(password, user.password):
        return
    return user


async def generate_password_reset_token(db: AsyncSession, phone: str, user: User) -> None:
    snmt = select(User).filter(User.number == phone)
    user_query = await db.execute(snmt)
    user = user_query.scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    reset_token = str(randint(100000, 999999))
    user.password_reset_token = reset_token
    user.reset_token_expires_at = datetime.utcnow() + timedelta(minutes=10)

    await db.commit()
    send_sms(phone, f"Your password reset code: {reset_token}")


async def reset_user_password(db: AsyncSession, phone: str, code: str, new_password: str) -> None:
    snmt = select(User).filter(User.number == phone)
    query_user = await db.execute(snmt)
    user = query_user.scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.password_reset_token != code or datetime.utcnow() > user.reset_token_expires_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")

    user.password = get_password_hash(new_password)
    user.password_reset_token = None
    user.reset_token_expires_at = None

    await db.commit()


async def change_user_password(db: AsyncSession, current_user: User, new_password: str) -> None:
    current_user.password = get_password_hash(new_password)
    await db.commit()


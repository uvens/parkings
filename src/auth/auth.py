from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from src.db import get_async_db_session
from src.auth.models import User
from src.setting import setting as settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="parking/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=settings.access_token_expire_days))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(db: AsyncSession, phone: str, password: str) -> Optional[User]:
    snmt = select(User).filter(User.number == phone)
    query_result = await db.execute(snmt)
    user = query_result.scalar()
    if not user or not verify_password(password, user.password):
        return None
    return user


async def get_current_user(db: AsyncSession = Depends(get_async_db_session),
                           token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    snmt = select(User).filter(User.id == int(user_id))
    user = await db.execute(snmt)
    user = user.scalar()
    if user is None:
        raise credentials_exception
    return user


async def get_superuser(user: User = Depends(get_current_user)) -> User:
    """ Проверка суперюзер или нет """
    if not user.is_super_user:
        raise HTTPException(
            status_code=403, detail='Permission Denied'
        )
    return user

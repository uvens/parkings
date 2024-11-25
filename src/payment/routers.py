from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from src.auth.models import User
from src.auth.auth import get_current_user, get_superuser
from src.db import get_async_db_session

from src.payment.services import payment_services

router = APIRouter(prefix='/payments', tags=['Payments'])


@router.post('/payment')
async def payment(db: AsyncSession = Depends(get_async_db_session),
                  user: User = Depends(get_current_user)):
    amount = 100
    return await payment_services.payment(amount=amount)


@router.get('/get_contract')
async def get_contract(db: AsyncSession = Depends(get_async_db_session),
                       user: User = Depends(get_current_user)):
    return await payment_services.get_contract(user)

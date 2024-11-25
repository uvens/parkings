from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from src.auth.models import User
from src.auth.auth import get_current_user, get_superuser
from src.db import get_async_db_session

from src.parcking.service import parking_services

router = APIRouter(prefix='/parkings', tags=['Parkings'])


@router.post('/create_parking')
async def create_parking(location_name: str,
                         total_spaces: int,
                         available_spaces: int,
                         price_per_hour: float, db: AsyncSession = Depends(get_async_db_session),
                         user: User = Depends(get_superuser)):
    return await parking_services.create_parking(db, location_name,
                                                 total_spaces,
                                                 available_spaces,
                                                 price_per_hour)


@router.get('/get_parking')
async def get_parking(parking_id: int, db: AsyncSession = Depends(get_async_db_session),
                      user: User = Depends(get_current_user)):
    return await parking_services.get_parking(db, parking_id)


@router.get('/get_all_parkings')
async def get_all_parkings(db: AsyncSession = Depends(get_async_db_session),
                           user: User = Depends(get_current_user)):
    return await parking_services.get_all_parkings(db)


@router.patch('/update_parking')
async def update_parking(parking_lot_id: int, price_per_month: float, db: AsyncSession = Depends(get_async_db_session),
                         user: User = Depends(get_current_user)):
    return await parking_services.update_parking(db, parking_lot_id, price_per_month)


@router.delete('/delete_parking')
async def delete_parking(parking_lot_id: int, db: AsyncSession = Depends(get_async_db_session),
                         user: User = Depends(get_current_user)):
    return await parking_services.delete_parking(db, parking_lot_id=parking_lot_id)


@router.get('/search_parking_name')
async def search_parking_name(location_name: str, db: AsyncSession = Depends(get_async_db_session),
                              user: User = Depends(get_current_user)):
    return await parking_services.search_parking_name(location_name, db)

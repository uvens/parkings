from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth import get_current_user
from src.db import get_async_db_session
from src.auth.models import User
from src.booking.models import ParkingBooking
from src.booking.schemas import BookingRequest
from src.booking.service import parking_booking_service

router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.get('/list_bookings')
async def list_bookings(db: AsyncSession = Depends(get_async_db_session), user: User = Depends(get_current_user)):
    return await parking_booking_service.list_bookings(db, user)


@router.get('/get_booking')
async def get_booking(booking_id: int, db: AsyncSession = Depends(get_async_db_session),
                      user: User = Depends(get_current_user)):
    return await parking_booking_service.get_booking(booking_id, db, user)


@router.post('/create_booking')
async def create_booking(booking_request: BookingRequest, db: AsyncSession = Depends(get_async_db_session),
                         user: User = Depends(get_current_user)):
    return await parking_booking_service.create_booking(booking_request=booking_request, db=db, user=user)


@router.delete('/delete_booking')
async def delete_booking(booking_id: int, db: AsyncSession = Depends(get_async_db_session),
                         user: User = Depends(get_current_user)):
    return await parking_booking_service.delete_booking(booking_id, db, user)

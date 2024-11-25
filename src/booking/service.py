from collections import defaultdict
from datetime import datetime, timedelta as td, timezone
from dateutil.relativedelta import relativedelta

from src.auth.models import User
from sqlalchemy import desc, literal, select, func, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select
from sqlalchemy.ext.asyncio import AsyncSession
from src.booking.models import ParkingBooking
from src.booking.schemas import BookingRequest
from src.parcking.models import ParkingLot
from fastapi import Depends
from src.auth.auth import get_current_user
from src.db import get_db_session


class ParkingBookingService:

    async def list_bookings(self,
                            db: AsyncSession,
                            user: User = Depends(get_current_user)):
        snmt = Select(ParkingBooking).filter(ParkingBooking.user_id == user.id)
        query = await db.execute(snmt)
        query_result = query.scalars().all()
        return query_result

    async def get_booking(self, booking_id: int, db: AsyncSession,
                          user: User = Depends(get_current_user)):
        snmt = Select(ParkingBooking).where(ParkingBooking.id == booking_id)
        query = await db.execute(snmt)
        query_result = query.scalars().all()
        return query_result

    @staticmethod
    def generate_booking(**bookings):
        booking = ParkingBooking(user_id=bookings.get('user_id'),
                                 parking_lot_id=bookings.get('parking_lot_id'),
                                 vehicle_type_id=bookings.get('vehicle_type_id'),
                                 vehicle_number=bookings.get('vehicle_number'),
                                 booking_start=bookings.get('booking_start'),
                                 booking_end=bookings.get('booking_end'),
                                 booking_type=bookings.get('booking_type'),
                                 booking_duration=bookings.get('booking_duration'),
                                 total_price=bookings.get('total_price'),
                                 status=bookings.get('status'))
        return booking

    @staticmethod
    async def get_count_available_spaces_parking(db: AsyncSession, parking_lot_id: int):
        snmt = select(ParkingLot).filter(ParkingLot.id == parking_lot_id)
        instance = await db.execute(snmt)
        instance = instance.scalar_one_or_none()
        if not instance:
            raise Exception('Нет парковки')
        return instance

    async def create_booking(self, booking_request: BookingRequest, db: AsyncSession,
                             user: User = Depends(get_current_user)):
        parking_lot: ParkingLot = await self.get_count_available_spaces_parking(db,
                                                                                booking_request.parking_lot_id)
        if parking_lot and parking_lot.available_spaces < 0:
            raise Exception('Нет свободных парковочных мест')
        booking_request.user_id = user.id
        booking = self.generate_booking(**booking_request.dict())
        if booking.booking_start.tzinfo is None or booking.booking_end.tzinfo:
            booking.booking_start = datetime.utcnow()
            booking.booking_end = datetime.utcnow() + relativedelta(months=1)
        db.add(booking)
        await db.commit()
        await db.refresh(booking)
        parking_lot.available_spaces -= booking.booking_duration
        db.add(parking_lot)
        await db.commit()
        await db.refresh(parking_lot)


async def delete_booking(self, booking_id, db: AsyncSession,
                         user: User = Depends(get_current_user)):
    snmt = select(ParkingBooking).filter(ParkingBooking.id == booking_id)
    instance = await db.execute(snmt)
    instance = instance.scalar_one_or_none()
    if instance:
        await db.delete(instance)
        await db.commit()


parking_booking_service = ParkingBookingService()

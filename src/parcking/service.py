from collections import defaultdict
from datetime import datetime, timedelta as td, timezone

from sqlalchemy import desc, literal, select, func, and_
from sqlalchemy.sql import Select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate_query
from src.parcking.models import ParkingLot


class ParkingServices:
    async def create_parking(self, db: AsyncSession, location_name: str,
                             total_spaces: int,
                             available_spaces: int,
                             price_per_hour: float):
        parking = ParkingLot(location_name=location_name, total_spaces=total_spaces,
                             available_spaces=available_spaces, price_per_hour=price_per_hour)

        db.add(parking)
        await db.commit()
        await db.refresh(parking)
        return {f'create_object : {parking.location_name}'}

    async def get_parking(self, db: AsyncSession, parking_id: int):
        snmt = select(ParkingLot).filter(ParkingLot.id == parking_id)
        query_result = await db.execute(snmt)
        result = query_result.scalar_one_or_none()
        return result

    async def get_all_parkings(self, db: AsyncSession):
        snmt = select(ParkingLot)
        query_result = await db.execute(snmt)
        result = query_result.scalars().all()
        return result

    async def update_parking(self, db: AsyncSession, parking_lot_id: int,
                             price_per_month: float):
        snmt = Select(ParkingLot).filter(ParkingLot.id == parking_lot_id)
        query_result = await db.execute(snmt)
        instance: ParkingLot = query_result.scalar()
        instance.total_spaces = price_per_month
        db.add(instance)
        await db.commit()
        await db.refresh(instance)

    async def delete_parking(self, db: AsyncSession, parking_lot_id: int):
        snmt = Select(ParkingLot).filter(ParkingLot.id == parking_lot_id)
        query_result = await db.execute(snmt)
        instance: ParkingLot = query_result.scalar()
        await db.delete(instance)
        await db.commit()

    async def search_parking_name(self, location_name: str, db: AsyncSession):
        snmt = select(ParkingLot).filter(ParkingLot.location_name.ilike(f"{location_name}"))
        query_result = await db.execute(snmt)
        result = query_result.scalars()
        if result:
            return result
        return []


parking_services = ParkingServices()

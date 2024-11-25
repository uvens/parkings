from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime
from pydantic.main import BaseModel


class ParkingBookingsSchema(BaseModel):
    id: int
    user_id: int
    parking_lot_id: int
    vehicle_type_id: str
    vehicle_number: str
    booking_start: datetime
    booking_end: datetime
    booking_type: str
    booking_duration: int
    total_price: float
    status: str
    created_at: datetime


class ParkingBookingsListSchema(BaseModel):
    result: List[ParkingBookingsSchema]


class BookingRequest(BaseModel):
    user_id: Optional[int]
    parking_lot_id: int
    vehicle_type_id: str
    vehicle_number: str
    booking_start: datetime
    booking_end: datetime
    booking_type: str
    booking_duration: int
    total_price: float
    status: str

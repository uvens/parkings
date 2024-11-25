import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Base, TrackableMixin

from src.db import async_session


class ParkingBooking(Base, TrackableMixin):
    __tablename__ = 'parking_bookings'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    parking_lot_id = sa.Column(sa.Integer, sa.ForeignKey('parking_lots.id', ondelete='CASCADE'), primary_key=True)
    vehicle_type = sa.Column(sa.String(length=20), nullable=True)
    vehicle_number = sa.Column(sa.String(length=20), nullable=True)
    booking_start = sa.Column(sa.DateTime, nullable=True)
    booking_end = sa.Column(sa.DateTime, nullable=True)
    booking_duration = sa.Column(sa.Integer, nullable=True)
    total_price = sa.Column(sa.Numeric(10, 2), nullable=True)
    status = sa.Column(sa.String(length=20), nullable=True)

    # user = sa.orm.relationship("User", back_populates="parking_bookings")
    # parking_lot = sa.orm.relationship("ParkingLot", back_populates="parking_bookings")

# @register(ParkingBooking, sqlalchemy_sessionmaker=async_session)
# class ParkingBookingAdmin(SqlAlchemyModelAdmin):
#     session: AsyncSession = async_session
#     # Поля, которые будут отображаться в списке объектов
#     list_display = (
#         "id",
#         "user_id",
#         "parking_lot_id",
#         "vehicle_type_id",
#         "vehicle_number",
#         "booking_start",
#         "booking_end",
#         "total_price",
#         "status"
#     )
#     # Ссылки для перехода на страницу редактирования объекта
#     list_display_links = ("id", "user_id", "parking_lot_id")
#     # Фильтры для удобного поиска
#     list_filter = ("status", "vehicle_type_id", "booking_start", "booking_end")
#     # Поля для поиска
#     search_fields = ("vehicle_number", "status")



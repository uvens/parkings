import sqlalchemy as sa

from src.core.models import Base, TrackableMixin
from src.db import async_session


class ParkingLot(Base, TrackableMixin):
    __tablename__ = 'parking_lots'

    id = sa.Column(sa.Integer, primary_key=True)
    location_name = sa.Column(sa.String(length=255), nullable=True)
    latitude = sa.Column(sa.Numeric(9, 6), nullable=True)
    longitude = sa.Column(sa.Numeric(9, 6), nullable=True)
    total_spaces = sa.Column(sa.Integer, nullable=True)
    available_spaces = sa.Column(sa.Integer, nullable=True)
    price_per_month = sa.Column(sa.Numeric(10, 2), nullable=True)

    def __str__(self):
        return self.location_name or f"Parking Lot {self.id}"


# @register(ParkingLot, sqlalchemy_sessionmaker=async_session)
# class ParkingLotAdmin(SqlAlchemyModelAdmin):
#     # Поля, которые будут отображаться в списке объектов
#     list_display = (
#         "id",
#         "location_name",
#         "latitude",
#         "longitude",
#         "total_spaces",
#         "available_spaces",
#         "price_per_month"
#     )
#     # Ссылки для перехода на страницу редактирования объекта
#     list_display_links = ("id",)
#     # Фильтры для удобного поиска
#     list_filter = ("location_name", "total_spaces", "available_spaces")
#     # Поля для поиска
#     search_fields = ("location_name",)

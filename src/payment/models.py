import sqlalchemy as sa
from src.core.models import Base


class Payment(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    booking_id = sa.Column(sa.Integer, sa.ForeignKey('parking_bookings.id', ondelete='CASCADE'), primary_key=True)
    amount = sa.Column(sa.Numeric(10, 2), nullable=True)
    payment_date = sa.Column(sa.DateTime, nullable=True)

    payment_method = sa.Column(sa.String(length=50), nullable=True)
    payment_status = sa.Column(sa.String(length=20), nullable=True)

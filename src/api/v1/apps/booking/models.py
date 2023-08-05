from apps.base_model import BaseModel
from db import db
from enum import Enum


class FlighSeatType(Enum):
    FIRST_CLASS = 1
    BUSINESS = 2


class Booking(BaseModel):
    __tablename__ = 'bookings'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id_', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id_'), nullable=False)
    passenger_count = db.Column(db.Integer, nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    status = db.Column(db.String, nullable=True, default='pending')
    is_booked = db.Column(db.Boolean, default=False, nullable=False)
    type_of_seats = db.Column(db.Enum(FlighSeatType), nullable=False)

from db import db
from apps.base_model import BaseModel

class AirPort(BaseModel):
    __tablename__ = 'airports'

    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    flights_departure = db.relationship('Flight', backref='departure_airport', foreign_keys='Flight.departure_airport_id',  lazy=True)
    flights_arrival = db.relationship('Flight', backref='arrival_airport', foreign_keys='Flight.arrival_airport_id',  lazy=True)

    airlines = db.relationship('AirPlane', backref='airport', lazy=True)

class AirPlane(BaseModel):
    __tablename__ = 'airplanes'

    reg_number = db.Column(db.String, nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=True)
    economy_seats = db.Column(db.Integer, nullable=True)
    business_seats = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, nullable=True)
    description = db.Column(db.Text, nullable=True)
    airport_id = db.Column(db.Integer, db.ForeignKey('airports.id_'), nullable=True)
    flights = db.relationship('Flight', backref='airplane', lazy=True)


class Flight(BaseModel):
    __tablename__ = 'flights'

    airplane_id = db.Column(db.Integer, db.ForeignKey('airplanes.id_'), nullable=False)
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id_'), nullable=False)
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id_'), nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    price_per_seat = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    seat_available = db.Column(db.Integer, nullable=True)


class AirLines(BaseModel):
    name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.String(150), nullable=True)
    airport_id = db.Column(db.Integer, db.ForeignKey('airports.id_'), nullable=True)

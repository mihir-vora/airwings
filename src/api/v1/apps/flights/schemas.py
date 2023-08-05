from marshmallow import Schema, fields, validate, ValidationError, validates_schema
from apps.validates import (
    positive_integer,
    economy_seats_validator,
    business_seats_validator,
    add_business_seats_and_economy_seats_validator)
from datetime import datetime

class AirPortSchema(Schema):
    id_ = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    country = fields.Str(required=True, validate=validate.Length(max=100))
    city = fields.Str(required=True, validate=validate.Length(max=100))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class AirPlaneSchema(Schema):
    id_ = fields.Int(dump_only=True)
    reg_number = fields.Str(required=True)
    capacity = fields.Int(required=True, validate=positive_integer)
    economy_seats = fields.Int(required=True, validate=positive_integer)
    business_seats = fields.Int(required=True, validate=positive_integer)
    is_active = fields.Boolean(required=False, default=False)
    description = fields.Str(required=True)
    airport_id = fields.Int(required=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


    @validates_schema
    def validate_seats(self, data, **kwargs):
        economy_seats_validator(data)
        business_seats_validator(data)
        add_business_seats_and_economy_seats_validator(data)

class AirPortCitySchema(Schema):
    class Meta:
        fields = ('city',)

class FlightSchema(Schema):
    id_ = fields.Int(dump_only=True)
    airplane_id = fields.Int(required=True)
    departure_airport_id = fields.Int(required=True)
    arrival_airport_id = fields.Int(required=True)
    departure_date = fields.DateTime(required=True)
    arrival_date = fields.DateTime(required=True)
    is_approved = fields.Boolean(required=True, default=False)
    price_per_seat = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    departure_airport = fields.Nested(AirPortCitySchema)
    arrival_airport = fields.Nested(AirPortCitySchema)
    time_taken = fields.Method('calculate_flights_duration')
    def calculate_flights_duration(self, obj):
        departure_date = datetime.fromisoformat(str(obj.departure_date))
        arrival_date = datetime.fromisoformat(str(obj.arrival_date))
        time_difference = arrival_date - departure_date
        hours = time_difference.seconds // 3600
        minutes = (time_difference.seconds // 60) % 60
        return f"{hours}h - {minutes}m"


from marshmallow import Schema, fields, validate
from enum import Enum
class SeatType(Enum):
    FIRST_CLASS = "first class"
    BUSINESS = "business"
    ECONOMY = "economy"
class BookingSchema(Schema):
    id_ = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    flight_id = fields.Int(required=True)
    seat_number = fields.Int(required=True)
    is_booked = fields.Str(default=False)
    type_of_seats = fields.Str(required=True, validate=validate.OneOf([seat_type.value for seat_type in SeatType]))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)



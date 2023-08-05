from marshmallow import fields, validate, Schema

class FlightSearchSchema(Schema):
    origin = fields.Str(required=True)
    destination = fields.Str(required=True)
from marshmallow import ValidationError
def positive_integer(value):
    if value <= 0:
        raise ValidationError("Value must be a positive integer.")

def economy_seats_validator(data):
    if 'capacity' in data and 'economy_seats' in data:
        if data['economy_seats'] > data['capacity']:
            raise ValidationError("Economy seats cannot be greater than total capacity.")

def business_seats_validator(data):
    if 'capacity' in data and 'business_seats' in data:
        if data['business_seats'] > data['capacity']:
            raise ValidationError("Business seats cannot be greater than total capacity.")

def add_business_seats_and_economy_seats_validator(data):
    if 'economy_seats' in data and 'business_seats' in data:
        if (data['business_seats'] + data['economy_seats']) > data['capacity']:
            raise ValidationError("Business seats and economy seats cannot be greater than total capacity.")
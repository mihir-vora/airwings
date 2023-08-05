from flask_restful import Resource
from flask import request
from .models import Booking
from .schemas import BookingSchema
from marshmallow.exceptions import  ValidationError
from db import db
from apps.utils import AuthMixin
from apps.flights.models import Flight




class BookingViews(Resource, AuthMixin):
    def get(self):
        current_user_id = self.require_auth()
        booking = Booking.query.filter_by(user_id=current_user_id).all()
        return BookingSchema(many=True).dump(booking)
    def post(self):
        current_user_id = self.require_auth()
        booking_json_data = request.get_json()
        try:
            booking_data = BookingSchema().load(booking_json_data)
        except ValidationError as err:
            return {
                'errors': err.messages
            }

        if not Flight.query.get(booking_json_data['flight_id']):
            return {'message' : 'flight not exist!'}, 404

        booking_data['user_id'] = current_user_id
        booking = Booking(**booking_data)
        booking.save()
        return BookingSchema().dump(booking)

class BookingGetEditDeleteViews(Resource):
    def get(self, booking_id):
        current_user_id = self.require_auth()
        booking = Booking.query.get(booking_id)
        if not booking:
            return {
                'message' : 'booking details not found'
            }
        if booking.user_id != current_user_id:
            return {'message': 'Unauthorized to update this airport'}, 403
        return BookingSchema().dump(booking)
    def put(self, booking_id):
        current_user_id = self.require_auth()
        booking = Booking.query.get(booking_id)
        booking_json_data = request.get_json()

        if not booking:
            return {
                'message': 'booking details not found'
            }

        if booking.user_id != current_user_id:
            return {'message': 'Unauthorized to update this airport'}, 403

        try:
            booking_data = BookingSchema().load(booking_json_data)
        except ValidationError as err:
            return {
                'errors': err.messages
            }
        booking.user_id = 2
        booking.booking_date = booking_data['booking_date']
        booking.flights = booking_data['flights']
        booking.email_status = booking_data['email_status']

        db.session.commit()
        booking.save()
        return BookingSchema().dump(booking)
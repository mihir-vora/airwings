from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from apps.auth.models import User
from functools import wraps
from apps.flights.models import AirPort, AirPlane, Flight

def not_found_response(msg=None):
    return {'message': f'details not found'}, 404

def get_airport(airport_id):
    return AirPort.query.get(airport_id) is not None
def get_airplane(airplane_id):
    return AirPlane.query.get(airplane_id)
def get_flight(flight_id):
    return Flight.query.get(flight_id)
def get_airplane_reg_number_exist(reg_num):
    return AirPlane.query.filter_by(reg_number=reg_num).first()
def get_departure_arrival_airport_id(departure_airport_id, arrival_airport_id):
    return departure_airport_id == arrival_airport_id

def _check_airport_and_airplane_existence(departure_airport_id, arrival_airport_id, airplane_id):
    if not get_airport(departure_airport_id) or not get_airport(arrival_airport_id):
        return {'message': 'Invalid departure or arrival airport details!'}, 404

    if not get_airplane(airplane_id):
        return {'message': 'Invalid airplane details!'}, 403

    if departure_airport_id == arrival_airport_id:
        return {'message': 'Departure and arrival airports cannot be the same!'}

    airplane = AirPlane.query.get(airplane_id)
    if airplane.is_active == False:
        return {'message' : 'this airplane details not exists'}
    return None

def get_airport_by_id(table, id):
    obj = table.query.get(id)
    if not obj:
        return not_found_response()
    return obj

class AuthMixin:
    @jwt_required()
    def require_auth(self):
        try:
            verify_jwt_in_request()
            current_user_identity = get_jwt_identity()
            return current_user_identity
        except:
            return {
                'message' : 'Authentication Required'
            }, 401

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        role = kwargs.get('role')
        if role != 'admin':
            return {
                'message' : 'Denied Access'
            }, 403
        return fn(*args, **kwargs)
    return wrapper

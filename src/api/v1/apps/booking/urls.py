from flask import Blueprint
from db import api
from .views import (
    BookingViews,
    BookingGetEditDeleteViews)

booking_bp = Blueprint('flights', __name__)

api.add_resource(BookingViews, '/booking')
api.add_resource(BookingGetEditDeleteViews, '/booking/<booking_id>')

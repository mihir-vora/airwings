from flask import Blueprint
from db import api
from .views import FlightSearchView


flight_search = Blueprint('flight_search', __name__)

api.add_resource(FlightSearchView, '/flights/search')

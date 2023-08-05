from flask import Blueprint
from db import api
from .views import (
    AirPortView,
    AirPostGetEditDelete,
    AirPlanesView,
    AirPlaneGetEditDelete,
    FlightView,
    FlightGetEditDelete
)

flight_bp = Blueprint('flight', __name__, url_prefix='flights')

api.add_resource(AirPortView, '/airport')
api.add_resource(AirPostGetEditDelete, '/airport/<int:airport_id>')
api.add_resource(AirPlanesView, '/airplane')
api.add_resource(AirPlaneGetEditDelete, '/airplane/<int:airplane_id>')
api.add_resource(FlightView, '/flights')
api.add_resource(FlightGetEditDelete, '/flights/<int:flight_id>')

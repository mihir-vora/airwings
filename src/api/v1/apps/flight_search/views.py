from flask_restful import Resource
from apps.flights.schemas import FlightSchema
from apps.flights.models import Flight, AirPort
from flask import request
from marshmallow.exceptions import ValidationError
from .schemas import FlightSearchSchema
from sqlalchemy import func
from datetime import datetime


class FlightSearchView(Resource):
    def get(self):
        origin_destination_json_data = request.get_json()
        try:
            flight_search_schema = FlightSearchSchema().load(origin_destination_json_data)
        except ValidationError as err:
            return {'errors' : err.messages}

        origin_city = flight_search_schema['origin'].lower()
        destination_city = flight_search_schema['destination'].lower()

        origin_airport = AirPort.query.filter(func.lower(AirPort.city) == origin_city).first()
        destination_airport = AirPort.query.filter(func.lower(AirPort.city) == destination_city).first()

        if not origin_airport or not destination_airport:
            return {'message': 'Invalid origin or destination city'}, 400

        flights = Flight.query.filter_by(departure_airport_id=origin_airport.id_,
                                         arrival_airport_id=destination_airport.id_, is_approved=True)

        try:
            flight_schema = FlightSchema(many=True, exclude=('is_approved',)).dump(flights)
        except ValidationError as err:
            return {'errors' : err.messages}, 400

        if not flight_schema:
            return {'message' : 'flight not exist'}

        total_flights_search_result = flights.count()

        return {
            'seacrh_result' : total_flights_search_result,
            'flight_results' : flight_schema
        }



from flask import request
from .models import AirPort, AirPlane, Flight
from .schemas import AirPortSchema, AirPlaneSchema, FlightSchema
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from apps.utils import (
    AuthMixin,
    admin_required,
    get_airport,
    get_airplane,
    get_airplane_reg_number_exist,
    get_flight,
    get_departure_arrival_airport_id,
    _check_airport_and_airplane_existence
)
from sqlalchemy import desc
class AirPortView(Resource, AuthMixin):
    def get(self):
        airport_data = (
            AirPort.query.filter_by().order_by(desc(AirPort.created_at)).all()
        )
        return AirPortSchema(many=True).dump(airport_data)

    def post(self):
        airport_json_data = request.get_json()
        try:
            airports_data = AirPortSchema().load(airport_json_data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        airport_db_obj = AirPort(**airports_data)
        airport_db_obj.save()

        return AirPortSchema().dump(airport_db_obj)


class AirPostGetEditDelete(Resource, AuthMixin):
    def get(self, airport_id):
        airport = AirPort.query.get(airport_id)
        if not airport:
            return {"message": f"details not found"}, 404
        return AirPortSchema().dump(airport)

    def put(self, airport_id):
        airport = AirPort.query.get(airport_id)
        if not airport:
            return {"message": f"details not found"}, 404

        flight_json_data = request.get_json()
        try:
            airport_data = AirPortSchema().load(flight_json_data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        airport.name, airport.city, airport.country = (
            airport_data["name"],
            airport_data["city"],
            airport_data["country"],
        )
        airport.update()
        return AirPortSchema().dump(airport)

    def delete(self, airport_id):
        airport = AirPort.query.get(airport_id)
        if not airport:
            return {"message": f"details not found"}, 404

        airport.delete()
        return {"message": "airport detail delete successfully"}


class AirPlanesView(Resource, AuthMixin):
    def get(self):
        airplane_data = AirPlane.query.all()
        if not airplane_data:
            return {"message": "there is not airplanes created yet!"}

        return AirPlaneSchema(many=True).dump(airplane_data)

    def post(self):
        airplane_json_data = request.get_json()

        if AirPlane.query.filter_by(
            reg_number=airplane_json_data["reg_number"]
        ).first():
            return {"message": "registration number already exists"}, 403

        try:
            airports_data = AirPlaneSchema().load(airplane_json_data)
        except ValidationError as err:
            return {"message": "Validation Error", "errors": err.messages}, 400

        airplane_db_obj = AirPlane(**airports_data)
        airplane_db_obj.save()

        return AirPlaneSchema().dump(airplane_db_obj)


class AirPlaneGetEditDelete(Resource, AuthMixin):
    def get(self, airplane_id):
        airplane = get_airplane(airplane_id)
        if not airplane:
            return {"message": f"details not found"}, 404
        return AirPlaneSchema().dump(airplane)

    def put(self, airplane_id):
        airplane = get_airplane(airplane_id)
        if not airplane:
            return {"message": f"details not found"}, 404

        airplane_json_data = request.get_json()
        if not get_airport(airplane_json_data["airport_id"]):
            return {"message": "airport details not found!"}

        try:
            airplane_data = AirPlaneSchema().load(airplane_json_data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        for key, value in airplane_data.items():
            setattr(airplane, key, value)

        airplane.update()
        return AirPlaneSchema().dump(airplane)

    def delete(self, airplane_id):
        airplane = get_airplane(airplane_id)
        if not airplane:
            return {"message": f"details not found"}, 404
        airplane.delete()
        return {"message": "airplane detail delete successfully"}


class FlightView(Resource):
    def get(self):
        flights = Flight.query.filter_by().all()
        if not flights:
            return {"messagee": "flights details not found!"}
        return FlightSchema(many=True).dump(flights)

    def post(self):
        flight_json_data = request.get_json()
        departure_airport_id = flight_json_data.get("departure_airport_id")
        arrival_airport_id = flight_json_data.get("arrival_airport_id")
        airplane_id = flight_json_data.get("airplane_id")

        errors = _check_airport_and_airplane_existence(
            departure_airport_id, arrival_airport_id, airplane_id
        )
        if errors:
            return errors
        try:
            flight_data = FlightSchema().load(flight_json_data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        flight = Flight(**flight_data)
        flight.save()

        return FlightSchema().dump(flight)

class FlightGetEditDelete(Resource):
    def get(self, flight_id):
        flight = get_flight(flight_id)
        if not flight:
            return {"message": f"details not found"}, 404
        return FlightSchema().dump(flight)

    def put(self, flight_id):
        flight = get_flight(flight_id)
        if not flight:
            return {"message": f"details not found"}, 404

        flight_json_data = request.get_json()
        departure_airport_id = flight_json_data.get("departure_airport_id")
        arrival_airport_id = flight_json_data.get("arrival_airport_id")
        airplane_id = flight_json_data.get("airplane_id")

        errors = _check_airport_and_airplane_existence(
            departure_airport_id, arrival_airport_id, airplane_id
        )
        if errors:
            return errors, errors["status_code"]
        try:
            flight_data = FlightSchema().load(flight_json_data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        for key, value in flight_data.items():
            setattr(flight, key, value)

        flight.update()
        return FlightSchema().dump(flight)
    def delete(self, flight_id):
        flight = get_flight(flight_id)
        if not flight:
            return {"message": f"details not found"}, 404
        flight.delete()
        return {"message": "flight detail delete successfully"}

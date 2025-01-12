from flask import g, request
from flask_restful import Resource

from .. import dao
from .. import db as dbm
from ..ext import db


class FlightCollectionResource(Resource):
    def post(self):
        data = request.get_json()

        req = dao.CreateFlightRequest(**data)

        flight = dbm.Flight(
            tenant_id=g.tenant.id,
            departure_icao=req.flight.departure_icao,
            arrival_icao=req.flight.arrival_icao,
            aircraft_id=req.flight.aircraft_id,
        )

        db.session.add(flight)
        db.session.commit()

        res = dao.CreateFlightResponse(
            **{
                "flight": {
                    "id": flight.id,
                    "departure_icao": flight.departure_icao,
                    "arrival_icao": flight.arrival_icao,
                    "aircraft_id": flight.aircraft_id,
                }
            }
        )

        return res.model_dump(), 201


class FlightResource(Resource):
    def get(self, flight_id):
        flight = db.session.get(dbm.Flight, flight_id)

        if not flight:
            return dao.Error(message="Flight not found").model_dump(), 404

        res = dao.GetFlightResponse(
            **{
                "flight": {
                    "id": flight.id,
                    "departure_icao": flight.departure_icao,
                    "arrival_icao": flight.arrival_icao,
                    "aircraft_id": flight.aircraft_id,
                }
            }
        )

        return res.model_dump()

    def put(self, flight_id):
        flight = db.session.get(dbm.Flight, flight_id)

        if not flight:
            return dao.Error(message="Flight not found").model_dump(), 404

        data = request.get_json()

        req = dao.UpdateFlightRequest(**data)

        if req.flight.id is not dao.empty:
            flight.id = req.flight.id
        if req.flight.departure_icao is not dao.empty:
            flight.departure_icao = req.flight.departure_icao
        if req.flight.arrival_icao is not dao.empty:
            flight.arrival_icao = req.flight.arrival_icao
        if req.flight.aircraft_id is not dao.empty:
            flight.aircraft_id = req.flight.aircraft_id

        db.session.commit()

        res = dao.UpdateFlightResponse(
            **{
                "flight": {
                    "id": flight.id,
                    "departure_icao": flight.departure_icao,
                    "arrival_icao": flight.arrival_icao,
                    "aircraft_id": flight.aircraft_id,
                }
            }
        )

        return res.model_dump()

    def delete(self, flight_id):
        flight = db.session.get(dbm.Flight, flight_id)

        if not flight:
            return dao.Error(message="Flight not found").model_dump(), 404

        db.session.delete(flight)
        db.session.commit()

        return "", 204

from flask import Blueprint, g, jsonify, request

from .. import dao
from .. import db as dbm
from ..ext import db

flights_bp = Blueprint("flights", __name__)


@flights_bp.route("/flights", methods=["POST"])
def create_flight():
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

    return jsonify(res.model_dump()), 201


@flights_bp.route("/flights/<int:flight_id>", methods=["GET"])
def get_flight(flight_id):
    flight = db.session.get(dbm.Flight, flight_id)

    if not flight:
        return jsonify(dao.Error(message="Flight not found").model_dump()), 404

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

    return jsonify(res.model_dump())


@flights_bp.route("/flights/<int:flight_id>", methods=["PUT"])
def update_flight(flight_id):
    flight = db.session.get(dbm.Flight, flight_id)

    if not flight:
        return jsonify(dao.Error(message="Flight not found").model_dump()), 404

    data = request.get_json()
    req = dao.UpdateFlightRequest(**data)

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

    return jsonify(res.model_dump())


@flights_bp.route("/flights/<int:flight_id>", methods=["DELETE"])
def delete_flight(flight_id):
    flight = db.session.get(dbm.Flight, flight_id)

    if not flight:
        return jsonify(dao.Error(message="Flight not found").model_dump()), 404

    db.session.delete(flight)
    db.session.commit()

    return "", 204

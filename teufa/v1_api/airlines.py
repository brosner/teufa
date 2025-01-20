from flask import Blueprint, g, jsonify, request

from .. import dao
from .. import db as dbm
from ..ext import db

bp = Blueprint("airlines", __name__, url_prefix="/airlines")


@bp.route("", methods=["POST"])
def create_airline():
    data = request.get_json()
    req = dao.CreateAirlineRequest(**data)

    airline = dbm.Airline(
        tenant_id=g.tenant.id,
        name=req.airline.name,
        iata=req.airline.iata,
        icao=req.airline.icao,
    )

    db.session.add(airline)
    db.session.commit()

    res = dao.CreateAirlineResponse(
        **{
            "airline": {
                "id": airline.id,
                "name": airline.name,
                "iata": airline.iata,
                "icao": airline.icao,
            }
        }
    )

    return jsonify(res.model_dump()), 201


@bp.route("/<int:airline_id>", methods=["GET"])
def get_airline(airline_id):
    airline = db.session.get(dbm.Airline, airline_id)

    if not airline:
        return jsonify(dao.Error(message="Airline not found").model_dump()), 404

    res = dao.GetAirlineResponse(
        **{
            "airline": {
                "id": airline.id,
                "name": airline.name,
                "iata": airline.iata,
                "icao": airline.icao,
            }
        }
    )

    return jsonify(res.model_dump())


@bp.route("/<int:airline_id>", methods=["PUT"])
def update_airline(airline_id):
    airline = db.session.get(dbm.Airline, airline_id)

    if not airline:
        return jsonify(dao.Error(message="Airline not found").model_dump()), 404

    data = request.get_json()
    req = dao.UpdateAirlineRequest(**data)

    if req.airline.name is not dao.empty:
        airline.name = req.airline.name
    if req.airline.iata is not dao.empty:
        airline.iata = req.airline.iata
    if req.airline.icao is not dao.empty:
        airline.icao = req.airline.icao

    db.session.commit()

    res = dao.UpdateAirlineResponse(
        **{
            "airline": {
                "id": airline.id,
                "name": airline.name,
                "iata": airline.iata,
                "icao": airline.icao,
            }
        }
    )

    return jsonify(res.model_dump())


@bp.route("/<int:airline_id>", methods=["DELETE"])
def delete_airline(airline_id):
    airline = db.session.get(dbm.Airline, airline_id)

    if not airline:
        return jsonify(dao.Error(message="Airline not found").model_dump()), 404

    db.session.delete(airline)
    db.session.commit()

    return "", 204

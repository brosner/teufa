import json

from flask import g
from flask.testing import FlaskClient
from sqlalchemy.sql import func, select

from teufa import db as dbm
from teufa.ext import db


def test_create_flight(client: FlaskClient):
    aircraft = dbm.Aircraft(
        tenant_id=g.tenant.id,
        icao="B737",
        tail_number="N12345",
        range_nm=3000,
    )
    db.session.add(aircraft)
    db.session.commit()

    response = client.post(
        "/api/v1/flights",
        json={
            "flight": {
                "departure_icao": "KDEN",
                "arrival_icao": "KLGA",
                "aircraft_id": aircraft.id,
            }
        },
    )

    assert response.status_code == 201
    assert json.loads(response.json) == {
        "flight": {
            "id": 1,
            "departure_icao": "KDEN",
            "arrival_icao": "KLGA",
            "aircraft_id": 1,
        }
    }


def test_get_flight(client: FlaskClient):
    aircraft = dbm.Aircraft(
        tenant_id=g.tenant.id,
        icao="B737",
        tail_number="N12345",
        range_nm=3000,
    )
    db.session.add(aircraft)
    db.session.commit()
    db.session.add(
        dbm.Flight(
            id=1,
            tenant_id=g.tenant.id,
            departure_icao="KDEN",
            arrival_icao="KLGA",
            aircraft_id=aircraft.id,
        )
    )
    db.session.commit()

    response = client.get("/api/v1/flights/1")

    assert response.status_code == 200
    assert json.loads(response.json) == {
        "flight": {
            "id": 1,
            "departure_icao": "KDEN",
            "arrival_icao": "KLGA",
            "aircraft_id": 1,
        }
    }


def test_get_flight_not_found(client: FlaskClient):
    response = client.get("/api/v1/flights/1")

    assert response.status_code == 404
    assert json.loads(response.json) == {"message": "Flight not found"}


def test_update_flight(client: FlaskClient):
    aircraft = dbm.Aircraft(
        tenant_id=g.tenant.id,
        icao="B737",
        tail_number="N12345",
        range_nm=3000,
    )
    db.session.add(aircraft)
    db.session.commit()
    db.session.add(
        dbm.Flight(
            id=1,
            tenant_id=g.tenant.id,
            departure_icao="KDEN",
            arrival_icao="KLGA",
            aircraft_id=aircraft.id,
        )
    )
    db.session.commit()

    response = client.put(
        "/api/v1/flights/1",
        json={
            "flight": {
                "departure_icao": "KJFK",
                "arrival_icao": "KLAX",
                "aircraft_id": 1,
            }
        },
    )

    assert response.status_code == 200
    assert json.loads(response.json) == {
        "flight": {
            "id": 1,
            "departure_icao": "KJFK",
            "arrival_icao": "KLAX",
            "aircraft_id": 1,
        }
    }


def test_update_flight_not_found(client: FlaskClient):
    response = client.put(
        "/api/v1/flights/1",
        json={
            "flight": {
                "departure_icao": "KJFK",
                "arrival_icao": "KLAX",
            }
        },
    )

    assert response.status_code == 404
    assert json.loads(response.json) == {"message": "Flight not found"}


def test_delete_flight(client: FlaskClient):
    aircraft = dbm.Aircraft(
        tenant_id=g.tenant.id,
        icao="B737",
        tail_number="N12345",
        range_nm=3000,
    )
    db.session.add(aircraft)
    db.session.commit()
    db.session.add(
        dbm.Flight(
            id=1,
            tenant_id=g.tenant.id,
            departure_icao="KDEN",
            arrival_icao="KLGA",
            aircraft_id=aircraft.id,
        )
    )
    db.session.commit()

    response = client.delete("/api/v1/flights/1")

    assert response.status_code == 204
    assert response.data == b""

    with db.session.begin():
        assert db.session.scalar(select(func.count(dbm.Flight.id))) == 0


def test_delete_flight_not_found(client: FlaskClient):
    response = client.delete("/api/v1/flights/1")

    assert response.status_code == 404
    assert json.loads(response.json) == {"message": "Flight not found"}

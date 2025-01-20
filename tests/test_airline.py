from flask.testing import FlaskClient
from sqlalchemy.sql import func, select

from teufa import db as dbm
from teufa.ext import db


def test_create_airline(client: FlaskClient, tenant: dbm.Tenant):
    response = client.post(
        "/api/v1/airlines",
        json={
            "airline": {
                "name": "Test Airline",
                "iata": "TA",
                "icao": "TST",
            }
        },
    )

    assert response.status_code == 201
    assert response.json == {
        "airline": {
            "id": 1,
            "name": "Test Airline",
            "iata": "TA",
            "icao": "TST",
        }
    }


def test_get_airline(client: FlaskClient, tenant: dbm.Tenant):
    airline = dbm.Airline(
        tenant_id=tenant.id,
        name="Test Airline",
        iata="TA",
        icao="TST",
    )
    db.session.add(airline)
    db.session.commit()

    response = client.get(f"/api/v1/airlines/{airline.id}")

    assert response.status_code == 200
    assert response.json == {
        "airline": {
            "id": airline.id,
            "name": "Test Airline",
            "iata": "TA",
            "icao": "TST",
        }
    }


def test_get_airline_not_found(client: FlaskClient):
    response = client.get("/api/v1/airlines/1")

    assert response.status_code == 404
    assert response.json == {"message": "Airline not found"}


def test_update_airline(client: FlaskClient, tenant: dbm.Tenant):
    airline = dbm.Airline(
        tenant_id=tenant.id,
        name="Test Airline",
        iata="TA",
        icao="TST",
    )
    db.session.add(airline)
    db.session.commit()

    response = client.put(
        f"/api/v1/airlines/{airline.id}",
        json={
            "airline": {
                "name": "Updated Airline",
                "iata": "UA",
                "icao": "UPD",
            }
        },
    )

    assert response.status_code == 200
    assert response.json == {
        "airline": {
            "id": airline.id,
            "name": "Updated Airline",
            "iata": "UA",
            "icao": "UPD",
        }
    }


def test_update_airline_not_found(client: FlaskClient):
    response = client.put(
        "/api/v1/airlines/1",
        json={
            "airline": {
                "name": "Updated Airline",
                "iata": "UA",
                "icao": "UPD",
            }
        },
    )

    assert response.status_code == 404
    assert response.json == {"message": "Airline not found"}


def test_delete_airline(client: FlaskClient, tenant: dbm.Tenant):
    airline = dbm.Airline(
        tenant_id=tenant.id,
        name="Test Airline",
        iata="TA",
        icao="TST",
    )
    db.session.add(airline)
    db.session.commit()

    response = client.delete(f"/api/v1/airlines/{airline.id}")

    assert response.status_code == 204
    assert response.data == b""

    with db.session.begin():
        assert db.session.scalar(select(func.count(dbm.Airline.id))) == 0


def test_delete_airline_not_found(client: FlaskClient):
    response = client.delete("/api/v1/airlines/1")

    assert response.status_code == 404
    assert response.json == {"message": "Airline not found"}

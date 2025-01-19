from flask.testing import FlaskClient
from sqlalchemy.sql import func, select

from teufa import db as dbm
from teufa.ext import db


def test_create_tenant(client: FlaskClient):
    response = client.post(
        "/api/v1/admin/tenants",
        json={
            "tenant": {
                "name": "Test Tenant",
                "hostname": "test.tenant.com",
            }
        },
    )

    assert response.status_code == 201
    assert response.json == {
        "tenant": {
            "id": 1,
            "name": "Test Tenant",
            "hostname": "test.tenant.com",
        }
    }


def test_get_tenant(client: FlaskClient):
    tenant = dbm.Tenant(
        name="Test Tenant",
        hostname="test.tenant.com",
    )
    db.session.add(tenant)
    db.session.commit()

    response = client.get(f"/api/v1/admin/tenants/{tenant.id}")

    assert response.status_code == 200
    assert response.json == {
        "tenant": {
            "id": tenant.id,
            "name": "Test Tenant",
            "hostname": "test.tenant.com",
        }
    }


def test_get_tenant_not_found(client: FlaskClient):
    response = client.get("/api/v1/admin/tenants/1")

    assert response.status_code == 404
    assert response.json == {"message": "Tenant not found"}


def test_update_tenant(client: FlaskClient):
    tenant = dbm.Tenant(
        name="Test Tenant",
        hostname="test.tenant.com",
    )
    db.session.add(tenant)
    db.session.commit()

    response = client.put(
        f"/api/v1/admin/tenants/{tenant.id}",
        json={
            "tenant": {
                "name": "Updated Tenant",
                "hostname": "updated.tenant.com",
            }
        },
    )

    assert response.status_code == 200
    assert response.json == {
        "tenant": {
            "id": tenant.id,
            "name": "Updated Tenant",
            "hostname": "updated.tenant.com",
        }
    }


def test_update_tenant_not_found(client: FlaskClient):
    response = client.put(
        "/api/v1/admin/tenants/1",
        json={
            "tenant": {
                "name": "Updated Tenant",
                "hostname": "updated.tenant.com",
            }
        },
    )

    assert response.status_code == 404
    assert response.json == {"message": "Tenant not found"}


def test_delete_tenant(client: FlaskClient):
    tenant = dbm.Tenant(
        name="Test Tenant",
        hostname="test.tenant.com",
    )
    db.session.add(tenant)
    db.session.commit()

    response = client.delete(f"/api/v1/admin/tenants/{tenant.id}")

    assert response.status_code == 204
    assert response.data == b""

    with db.session.begin():
        assert db.session.scalar(select(func.count(dbm.Tenant.id))) == 0


def test_delete_tenant_not_found(client: FlaskClient):
    response = client.delete("/api/v1/admin/tenants/1")

    assert response.status_code == 404
    assert response.json == {"message": "Tenant not found"}

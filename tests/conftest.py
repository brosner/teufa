import pytest
from flask import Flask, g
from flask.testing import FlaskClient

from teufa import db as dbm
from teufa.app import create_app
from teufa.ext import db


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        dbm.Base.metadata.create_all(db.engine)
        yield app
        dbm.Base.metadata.drop_all(db.engine)


@pytest.fixture
def tenant(app: Flask):
    tenant = dbm.Tenant(
        name="Default",
        hostname="localhost",
    )
    db.session.add(tenant)
    db.session.commit()

    return tenant


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

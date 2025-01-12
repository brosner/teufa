import pytest
from flask import Flask, current_app, g
from flask.testing import FlaskClient

from teufa import db as dbm
from teufa.app import create_app
from teufa.ext import db


def pytest_configure():
    app = create_app()
    app.app_context().push()


def create_default_tenant():
    tenant = dbm.Tenant(
        name="Default",
        hostname="localhost",
    )
    db.session.add(tenant)
    db.session.commit()

    g.tenant = tenant


@pytest.fixture
def app():
    dbm.Base.metadata.create_all(db.engine)

    with current_app.app_context():
        create_default_tenant()
        yield current_app

    dbm.Base.metadata.drop_all(db.engine)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

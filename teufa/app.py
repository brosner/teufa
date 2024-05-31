from flask import Flask, g, request
from sqlalchemy import select

from . import db as dbm
from .config import Config
from .ext import db
from .v1_api import bp as v1_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)

    @app.before_request
    def before_request():
        hostname = request.host.split(":")[0]
        g.tenant = db.session.scalars(
            select(dbm.Tenant).filter_by(hostname=hostname).limit(1)
        ).first()

    @app.teardown_request
    def teardown_request(exc):
        if exc:
            db.session.rollback()
        db.session.remove()

    app.register_blueprint(v1_bp)

    return app

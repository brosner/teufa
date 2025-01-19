from flask import Flask

from .config import Config
from .ext import db
from .v1_api import v1_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)

    @app.teardown_request
    def teardown_request(exc):
        if exc:
            db.session.rollback()
        db.session.remove()

    app.register_blueprint(v1_bp)

    @app.route("/healthz")
    def healthz():
        return {"status": "ok"}

    return app

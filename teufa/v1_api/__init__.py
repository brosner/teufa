from flask import Blueprint, Flask, g, request
from flask_restful import Api
from sqlalchemy import select

from ..ext import db
from . import db as dbm
from .flights import FlightCollectionResource, FlightResource

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.before_request
def before_request():
    if not hasattr(g, "tenant"):
        hostname = request.host.split(":")[0]
        g.tenant = db.session.scalars(
            select(dbm.Tenant).filter_by(hostname=hostname).limit(1)
        ).first()


api = Api(bp)

api.add_resource(FlightCollectionResource, "/v1/flights")
api.add_resource(FlightResource, "/v1/flights/<int:flight_id>")

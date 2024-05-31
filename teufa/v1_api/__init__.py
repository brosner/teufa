from flask import Blueprint
from flask_restful import Api

from .flights import FlightCollectionResource, FlightResource

bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)

api.add_resource(FlightCollectionResource, "/v1/flights")
api.add_resource(FlightResource, "/v1/flights/<int:flight_id>")

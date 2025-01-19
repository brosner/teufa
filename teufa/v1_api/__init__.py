from flask import Blueprint, g, request
from sqlalchemy import select

from .. import db as dbm
from ..ext import db
from .flights import flights_bp
from .tenants import tenants_bp

v1_bp = Blueprint("v1", __name__, url_prefix="/api/v1")

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

admin_bp.register_blueprint(tenants_bp)
v1_bp.register_blueprint(admin_bp)

api_bp = Blueprint("api", __name__, url_prefix="/")


@api_bp.before_request
def before_request():
    if not hasattr(g, "tenant"):
        hostname = request.host.split(":")[0]
        g.tenant = db.session.scalars(
            select(dbm.Tenant).filter_by(hostname=hostname).limit(1)
        ).first()


api_bp.register_blueprint(flights_bp)
v1_bp.register_blueprint(api_bp)

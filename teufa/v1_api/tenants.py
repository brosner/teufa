from flask import Blueprint, g, jsonify, request

from .. import dao
from .. import db as dbm
from ..ext import db

bp = Blueprint("tenants", __name__, url_prefix="/tenants")


@bp.route("", methods=["POST"])
def create_tenant():
    data = request.get_json()
    req = dao.CreateTenantRequest(**data)

    tenant = dbm.Tenant(
        name=req.tenant.name,
        hostname=req.tenant.hostname,
    )

    db.session.add(tenant)
    db.session.commit()

    res = dao.CreateTenantResponse(
        **{
            "tenant": {
                "id": tenant.id,
                "name": tenant.name,
                "hostname": tenant.hostname,
                "created_at": tenant.created_at,
            }
        }
    )

    return jsonify(res.model_dump()), 201


@bp.route("/<int:tenant_id>", methods=["GET"])
def get_tenant(tenant_id):
    tenant = db.session.get(dbm.Tenant, tenant_id)

    if not tenant:
        return jsonify(dao.Error(message="Tenant not found").model_dump()), 404

    res = dao.GetTenantResponse(
        **{
            "tenant": {
                "id": tenant.id,
                "name": tenant.name,
                "hostname": tenant.hostname,
                "created_at": tenant.created_at,
            }
        }
    )

    return jsonify(res.model_dump())


@bp.route("/<int:tenant_id>", methods=["PUT"])
def update_tenant(tenant_id):
    tenant = db.session.get(dbm.Tenant, tenant_id)

    if not tenant:
        return jsonify(dao.Error(message="Tenant not found").model_dump()), 404

    data = request.get_json()
    req = dao.UpdateTenantRequest(**data)

    if req.tenant.name is not dao.empty:
        tenant.name = req.tenant.name
    if req.tenant.hostname is not dao.empty:
        tenant.hostname = req.tenant.hostname

    db.session.commit()

    res = dao.UpdateTenantResponse(
        **{
            "tenant": {
                "id": tenant.id,
                "name": tenant.name,
                "hostname": tenant.hostname,
                "created_at": tenant.created_at,
            }
        }
    )

    return jsonify(res.model_dump())


@bp.route("/<int:tenant_id>", methods=["DELETE"])
def delete_tenant(tenant_id):
    tenant = db.session.get(dbm.Tenant, tenant_id)

    if not tenant:
        return jsonify(dao.Error(message="Tenant not found").model_dump()), 404

    db.session.delete(tenant)
    db.session.commit()

    return "", 204

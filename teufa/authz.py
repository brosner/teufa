from authlib.integrations.flask_oauth2 import AuthorizationServer, ResourceProtector
from authlib.integrations.sqla_oauth2 import (
    create_bearer_token_validator,
    create_query_client_func,
    create_revocation_endpoint,
    create_save_token_func,
)
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7636 import CodeChallenge
from flask import Blueprint, request

from . import db as dbm
from .ext import db

query_client = create_query_client_func(db.session, dbm.OAuth2Client)
save_token = create_save_token_func(db.session, dbm.OAuth2Token)


authz = AuthorizationServer(query_client=query_client, save_token=save_token)
bp = Blueprint("authz", __name__, url_prefix="/authz")
require_oauth = ResourceProtector()


def init_app(app):
    authz.init_app(app)

    authz.register_grant(AuthorizationCodeGrant, [CodeChallenge(required=True)])

    revocation_cls = create_revocation_endpoint(db.session, dbm.OAuth2Token)
    authz.register_endpoint(revocation_cls)

    bearer_cls = create_bearer_token_validator(db.session, dbm.OAuth2Token)
    require_oauth.register_token_validator(bearer_cls())

    app.register_blueprint(bp)


@bp.route("/oauth/authorize", methods=["GET", "POST"])
def authorize():
    if request.method == "GET":
        return (
            """
        <html>
            <body>
                <form method="post" action="/authz/oauth/authorize">
                    <button type="submit">Authorize</button>
                </form>
            </body>
        </html>
        """,
            200,
            {"Content-Type": "text/html"},
        )
    current_user = db.session.query(dbm.User).filter_by(name="default").first()
    if current_user:
        return authz.create_authorization_response(grant_user=current_user)
    else:
        return authz.create_authorization_response(grant_user=None)


@bp.route("/oauth/token", methods=["POST"])
def issue_token():
    return authz.create_token_response()


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        "client_secret_basic",
        "client_secret_post",
        "none",
    ]

    def save_authorization_code(self, code, request):
        code_challenge = request.data.get("code_challenge")
        code_challenge_method = request.data.get("code_challenge_method")
        auth_code = dbm.OAuth2AuthorizationCode(
            code=code,
            client_id=request.client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=request.user.id,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
        )
        db.session.add(auth_code)
        db.session.commit()
        return auth_code

    def query_authorization_code(self, code, client):
        auth_code = (
            db.session.query(dbm.OAuth2AuthorizationCode)
            .filter_by(code=code, client_id=client.client_id)
            .first()
        )
        if auth_code and not auth_code.is_expired():
            return auth_code

    def delete_authorization_code(self, authorization_code):
        db.session.delete(authorization_code)
        db.session.commit()

    def authenticate_user(self, authorization_code):
        return db.session.query(dbm.User).get(authorization_code.user_id)

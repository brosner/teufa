import os
import sys
import time

import click
from werkzeug.security import gen_salt

import alembic.config
import teufa.server
from teufa import db as dbm
from teufa.app import create_app
from teufa.ext import db


@click.group()
def cli():
    pass


@cli.command()
@click.option("--dev/--no-dev", default=False)
def server(dev):
    port = os.environ.get("PORT", 8000)
    cfg = {
        "bind": f"0.0.0.0:{port}",
        "reload": dev,
    }
    teufa.server.Application(cfg).run()


@cli.command(
    "alembic",
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    },
    add_help_option=False,
)
def run_alembic(*args, **kwargs):
    alembic.config.main(prog="teufa alembic", argv=sys.argv[2:])


@cli.command()
@click.argument("client_name")
@click.argument("client_uri")
@click.argument("redirect_uri")
def create_oauth_client(client_name, client_uri, redirect_uri):
    app = create_app()
    with app.app_context():
        client_id = gen_salt(24)
        client_id_issued_at = int(time.time())
        client = dbm.OAuth2Client(
            client_id=client_id,
            client_id_issued_at=client_id_issued_at,
        )

        # possible values: none, client_secret_basic or client_secret_post
        token_endpoint_auth_method = "client_secret_basic"

        client.set_client_metadata(
            {
                "client_name": client_name,
                "client_uri": client_uri,
                "grant_types": ["authorization_code"],
                "redirect_uris": [redirect_uri],
                "response_types": [],
                "scope": "profile",
                "token_endpoint_auth_method": token_endpoint_auth_method,
            }
        )

        if token_endpoint_auth_method == "none":
            client.client_secret = ""
        else:
            client.client_secret = gen_salt(48)

        db.session.add(client)
        db.session.commit()

        click.echo(f"Created OAuth client: {client_name}")

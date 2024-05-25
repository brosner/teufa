import os
import sys

import click

import alembic.config
import teufa.server


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

import click
import teufa.server


@click.group()
def cli():
    pass


@cli.command()
@click.option("--dev/--no-dev", default=False)
def server(dev):
    cfg = {
        "bind": "127.0.0.1:8000",
        "reload": dev,
    }
    teufa.server.Application(cfg).run()


@cli.command()
def initdb():
    click.echo("Initialized the database")

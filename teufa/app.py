from flask import Flask

from .ext import db


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

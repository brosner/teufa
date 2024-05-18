from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["A"] = 1
    return app

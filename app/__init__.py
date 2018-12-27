from flask import Flask
from ..config import config #top level file


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

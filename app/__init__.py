from flask import Flask
from flask_bootstrap import Bootstrap
from ..config import config #top level file
from flask_moment import Moment

bootstrap = Bootstrap()
moment = Moment()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

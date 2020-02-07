from sanic import Sanic

from . import config, extensions
from .blueprints import blueprint, blueprint_exceptions


def create_app(config_object: object = config.Config) -> Sanic:
    app = Sanic()
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app: Sanic):
    extensions.register_redis(app)


def register_blueprints(app: Sanic):
    app.blueprint(blueprint)
    app.blueprint(blueprint_exceptions)

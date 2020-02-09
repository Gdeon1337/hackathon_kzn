from sanic import Sanic, Blueprint

from . import config, extensions
from .blueprints import blueprint, blueprint_exceptions, blueprint_photos


def create_app(config_object: object = config.Config) -> Sanic:
    app = Sanic()
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app: Sanic):
    extensions.register_db(app)
    extensions.register_redis(app)
    extensions.register_cors(app)


def register_blueprints(app: Sanic):
    app.blueprint(Blueprint.group(
        blueprint_photos,
        blueprint,
        blueprint_exceptions
    ))

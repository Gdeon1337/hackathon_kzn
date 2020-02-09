from sanic import Sanic
from database import db
from .redis_conn import RedisConn
from sanic_cors import CORS
# from .blueprints.answers.view import cre, crea_dialog


conn = RedisConn()


def register_redis(app: Sanic):
    app.register_listener(conn.create_redis_connection, 'before_server_start')
    # app.register_listener(crea_dialog, 'after_server_start')
    app.register_listener(conn.close_redis_connection, 'before_server_stop')


def register_db(app: Sanic):
    app.config.DB_DSN = app.config.PG_CONNECTION
    app.config.DB_ECHO = app.config.DEBUG
    db.init_app(app)
    app.db = db


def register_cors(app: Sanic):
    app.cors = CORS(app)

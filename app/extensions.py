from sanic import Sanic

from .redis_conn import RedisConn


conn = RedisConn()


def register_redis(app: Sanic):
    app.register_listener(conn.create_redis_connection, 'before_server_start')
    app.register_listener(conn.close_redis_connection, 'before_server_stop')

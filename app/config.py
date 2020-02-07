import os
from typing import Tuple

import toml
from sanic_envconfig import EnvConfig


app_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(app_dir, os.pardir))
pyproject_info = toml.load(os.path.join(project_root, 'pyproject.toml'))
poetry_info = pyproject_info['tool']['poetry']

app_name = poetry_info["name"].lower()
service_name = f'{app_name}'

default_ip = 'localhost'
default_redis_conn = 'redis://localhost:6379/1'


class Config(EnvConfig):
    SERVER_IP: str = default_ip
    SERVER_PORT: int = 80
    REDIS_CONNECTION: str = default_redis_conn

    APP_DIR: str = app_dir
    PROJECT_ROOT: str = project_root

    IS_DOCKER: bool = False

    APP_NAME: str = app_name
    SERVICE_NAME: str = service_name
    API_TITLE: str = service_name.title()
    API_VERSION: str = poetry_info['version']
    API_DESCRIPTION: str = poetry_info['description']
    API_SCHEMES: Tuple[str] = ('http', 'https')

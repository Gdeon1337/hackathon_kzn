from sanic import Blueprint
from sanic.request import Request
from sanic.response import json


blueprint = Blueprint('answers', url_prefix='/', strict_slashes=True)


@blueprint.post('/')
async def domain(request: Request):
    return json({'status': 'ok'})


@blueprint.get('/')
async def get_currency(request: Request):
    return json({'answers': '', 'status': 'ok'})

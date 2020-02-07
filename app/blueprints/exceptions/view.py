from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import InvalidUsage


blueprint_exceptions = Blueprint('except', url_prefix='/', strict_slashes=True)


@blueprint_exceptions.exception(InvalidUsage)
def except_invalid_usage(requests: Request, exceptions):  # pylint: disable=unused-argument
    return json({
        'status': str(exceptions)
    }, status=400)

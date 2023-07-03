from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .const import (
    EMPTY_BODY_MASSEGE,
)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    url = URLMap()
    data = request.get_json()
    if type(data) != dict:
        raise InvalidAPIUsage(EMPTY_BODY_MASSEGE)
    url.save(data)
    return jsonify(url.from_dict(data).to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_short_url(short_id):
    short_map = URLMap.get(short_id)
    if short_map is not None:
        return jsonify({'url': short_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

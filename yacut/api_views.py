from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .const import (
    EMPTY_BODY_MASSEGE,
    URL_IS_NECESSARILY_MESSAGE
)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if type(data) != dict:
        raise InvalidAPIUsage(EMPTY_BODY_MASSEGE)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_IS_NECESSARILY_MESSAGE)
    url_map = URLMap.from_dict(data)
    url_map.save()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_short_url(short_id):
    short_map = URLMap.get(short_id)
    if short_map is not None:
        return jsonify({'url': short_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

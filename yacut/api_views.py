from http import HTTPStatus
import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .const import (
    EMPTY_BODY_MASSEGE,
    URL_IS_NECESSARILY_MESSAGE,
    NOT_CORREKR_BODY_MESSAGE,
    PATTERN,
    NAME_TAKEN_MASSEGE_FIRST_PATH,
    NAME_TAKEN_MASSEGE_SECOND_PATH
)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    url = URLMap()
    if type(data) != dict:
        raise InvalidAPIUsage(EMPTY_BODY_MASSEGE)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_IS_NECESSARILY_MESSAGE)
    if 'custom_id' in data:
        custom_id = data.get('custom_id')
        if not url.check_short_id_on_unic(custom_id):
            raise InvalidAPIUsage(f'{NAME_TAKEN_MASSEGE_FIRST_PATH}"{custom_id}"{NAME_TAKEN_MASSEGE_SECOND_PATH}')
        if custom_id == '' or custom_id is None:
            data['custom_id'] = url.get_unique_short_id()
        elif not re.match(PATTERN, custom_id):
            raise InvalidAPIUsage(NOT_CORREKR_BODY_MESSAGE)
    else:
        data['custom_id'] = url.get_unique_short_id()
    urlmap = URLMap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_short_url(short_id):
    short_map = URLMap.get(short_id)
    if short_map is not None:
        return jsonify({'url': short_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

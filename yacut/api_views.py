from http import HTTPStatus

from flask import jsonify, request
import pyshorteners

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=('POST',))
def get_unique_short_id():
    urls = URLMap()
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    original_url = data.get('original', 'Ошибка')
    short_url = pyshorteners.Shortener().tinyurl.short(original_url)
    db.session.add(
        URLMap(
            original=original_url,
            short=short_url,
        )
    )
    db.session.commit()
    return jsonify({'urls': urls.to_dict()}), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_short_url(short_id):
    short_map = URLMap.query.filter_by(short=short_id).first()
    if short_map is not None:
        return jsonify({'url': short_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage('Такого нет', HTTPStatus.NOT_FOUND)

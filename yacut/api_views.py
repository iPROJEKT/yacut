from http import HTTPStatus
import random
from string import ascii_letters, digits
import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


def check_short_id_on_unic(custom_id):
    if URLMap.query.filter_by(short=custom_id).first():
        return False
    if re.match(r'^[a-zA-Z\d]{1,16}$', custom_id) is None:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    return True


def get_unique_short_id():
    custom_id = ''
    for _ in range(6):
        custom_id.join(random.choice(ascii_letters + digits))
    if check_short_id_on_unic(custom_id):
        return get_unique_short_id
    return custom_id


@app.route('/api/id/', methods=('POST',))
def get_unique_short():
    url = URLMap()
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    original_url = data.get('url')
    if 'short_link' in data:
        short_link = data.get('short_link`')
        if not check_short_id_on_unic(short_link):
            raise InvalidAPIUsage(f'Имя "{short_link}" уже занято.')
        if short_link == '' or short_link is None:
            with_sh_l = URLMap(
                original=original_url,
                short=short_link,
            )
            db.session.add(with_sh_l)
    not_sh_l = URLMap(
        original=original_url,
        short=get_unique_short_id(),
    )
    db.session.add(not_sh_l)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED



@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_short_url(short_id):
    short_map = URLMap.query.filter_by(short=short_id).first()
    if short_map is not None:
        return jsonify({'url': short_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage(f'Указанный id не найден', HTTPStatus.NOT_FOUND)

from http import HTTPStatus
import random
from string import ascii_letters, digits
import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


def chek_on_sumvols(short_link):
    if re.match(r'^[a-zA-Z\d]{1,16}$', short_link) is None:
        return False
    return True


def check_short_id_on_unic(short_link):
    if URLMap.query.filter_by(short=short_link).first():
        return False
    return True


def get_unique_short_id():
    short_link = ''.join(random.choice(ascii_letters + digits) for _ in range(6))
    if check_short_id_on_unic(short_link) == False:
        return get_unique_short_id()
    return short_link


@app.route('/api/id/', methods=('POST',))
def get_unique_short():
    url = URLMap()
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    op = data.get('url')
    if 'url' not in data or op == '':
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'short_link' in data:
        short_link = data.get('short_link')
        if check_short_id_on_unic(short_link) == False:
            raise InvalidAPIUsage(f'Имя "{short_link}" уже занято.')
        if chek_on_sumvols(short_link) == False:
            raise InvalidAPIUsage(f'Указано недопустимое имя для короткой ссылки')
        if short_link == '' or short_link is None:
            w_l = URLMap(
                original=op,
                short=short_link
            )
            db.session.add(w_l)
    else:
        n_l = URLMap(
            original=op,
            short=get_unique_short_id()
        )
        db.session.add(n_l)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED



@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_short_url(short_id):
    short_map = URLMap.query.filter_by(short=short_id).first()
    if short_map is not None:
        return jsonify({'url': short_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage(f'Указанный id не найден', HTTPStatus.NOT_FOUND)

from datetime import datetime
import re
from http import HTTPStatus

import pyshorteners
from flask import url_for

from .error_handlers import InvalidAPIUsage
from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        for field in ['id', 'original', 'short', 'timestamp']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.short,
        )

    def valid_short_url(self, short_id):
        if len(short_id) > 16:
            return False
        for value in short_id:
            if re.match(r'^[a-zA-Z\d]{1,16}$', value) is None:
                raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        return True

    def get_unic_short_link(self, original_url):
        short_id = pyshorteners.Shortener().tinyurl.short(original_url)
        if URLMap.query.filter_by(short=short_id).first():
            raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.', HTTPStatus.BAD_REQUEST)
        if not URLMap.valid_short_url(self, short_id):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', HTTPStatus.BAD_REQUEST)
        return f'http://localhost/{short_id}', HTTPStatus.CREATED

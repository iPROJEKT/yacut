from datetime import datetime
import random
import re

from flask import url_for

from .error_handlers import InvalidAPIUsage
from .const import (
    PATTERN,
    PATTERN_FOR_GEN_URK,
    DICT_LABELS,
    NAME_TAKEN_MASSEGE_FIRST_PATH,
    NAME_TAKEN_MASSEGE_SECOND_PATH,
    NOT_CORREKR_BODY_MESSAGE
)
from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(filter_by_obj):
        return URLMap.query.filter_by(short=filter_by_obj).first()

    @staticmethod
    def get_or_404(filter_by_obj):
        return URLMap.query.filter_by(short=filter_by_obj).first_or_404()

    @staticmethod
    def character_check(short_link):
        if re.match(PATTERN, short_link) is None:
            return False
        return True

    @staticmethod
    def check_short_id_on_unique(short_link):
        if URLMap.get(short_link):
            return False
        return True

    @staticmethod
    def get_unique_short_id():
        short_link = ''.join(random.choice(PATTERN_FOR_GEN_URK) for _ in range(6))
        if not URLMap.check_short_id_on_unique(short_link):
            raise InvalidAPIUsage('Число подменных url достигла ')
        return short_link

    @staticmethod
    def from_dict(data):
        instance = URLMap()
        if 'custom_id' in data:
            custom_id = data.get('custom_id')
            if not URLMap.check_short_id_on_unique(custom_id):
                raise InvalidAPIUsage(f'{NAME_TAKEN_MASSEGE_FIRST_PATH}"{custom_id}"{NAME_TAKEN_MASSEGE_SECOND_PATH}')
            if custom_id == '' or custom_id is None:
                data['custom_id'] = URLMap.get_unique_short_id()
            elif not re.match(PATTERN, custom_id):
                raise InvalidAPIUsage(NOT_CORREKR_BODY_MESSAGE)
        else:
            data['custom_id'] = URLMap.get_unique_short_id()
        for field_db, field_inp in DICT_LABELS.items():
            if field_inp in data:
                setattr(instance, field_db, data[field_inp])
        return instance

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

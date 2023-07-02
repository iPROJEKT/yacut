from datetime import datetime
import random
import re

from flask import url_for

from .error_handlers import InvalidAPIUsage
from .const import PATTERN, PATTERN_FOR_GEN_URK, DICT_LABELS
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

    def check_short_id_on_unic(self, short_link):
        if URLMap.query.filter_by(short=short_link).first():
            return False
        return True

    def get_unique_short_id(self):
        short_link = ''.join(random.choice(PATTERN_FOR_GEN_URK) for _ in range(6))
        if not self.check_short_id_on_unic(short_link):
            raise InvalidAPIUsage('Число подменных url достигла ')
        return short_link

    @staticmethod
    def from_dict(data):
        instance = URLMap()
        for field_db, field_inp in DICT_LABELS.items():
            if field_inp in data:
                setattr(instance, field_db, data[field_inp])
        return instance

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short
        )

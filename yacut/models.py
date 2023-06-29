from datetime import datetime
import random
from string import ascii_letters, digits
import re

from flask import url_for

from .const import PATTERN
from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        for field_db, field_inp in {'original': 'url', 'short': 'custom_id'}.items():
            if field_inp in data:
                setattr(self, field_db, data[field_inp])

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short
        )

    def chek_on_sumvols(self, short_link):
        if re.match(PATTERN, short_link) is None:
            return False
        return True

    def check_short_id_on_unic(self, short_link):
        if URLMap.query.filter_by(short=short_link).first():
            return False
        return True

    def get_unique_short_id(self):
        short_link = ''.join(random.choice(ascii_letters + digits) for _ in range(6))
        if not self.check_short_id_on_unic(short_link):
            return self.get_unique_short_id()
        return short_link

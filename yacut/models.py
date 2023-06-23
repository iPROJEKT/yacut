from datetime import datetime
import re

from flask import url_for

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
            short_link=self.short
        )

    def valid_short_url(self, short_id):
        if len(short_id) > 16:
            return False
        for value in short_id:
            if re.match(r'^a-zA-Z0-9_', value) is None:
                return False
        return True

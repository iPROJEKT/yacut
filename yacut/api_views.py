from flask import jsonify

from . import app
from .models import URLMap


def opinion_to_dict(opinion):
    return dict(
        id = opinion.id,
        original = opinion.original,
        short = opinion.short,
        timestamp = opinion.timestamp,
    )


@app.route('/api/id/', methods=['POST'])  
def get_unique_short_id():
    opinion = URLMap.query.get_or_404(id)
    data = opinion_to_dict(opinion)  
    return jsonify(
        {'opinion': data}
    ), 200

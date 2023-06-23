from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from yacut import app
from .forms import UrlForm
from .models import URLMap

@app.route('/', methods=('GET', 'POST',))
def index_view():
    form = UrlForm()
    return render_template('urls.html', form=form)


@app.route('/<string:short_id>', methods=('GET',))
def short_link_url(short_id):
    return redirect(
        URLMap.query.filter_by(
            short=short_id
        ).first_or_404().original
    )

from http import HTTPStatus

from flask import render_template, flash, redirect

from yacut import app, db
from .forms import UrlForm
from .models import URLMap
from .api_views import get_unique_short_id, check_short_id_on_unic, chek_on_sumvols


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('urls.html', form=form)
    short_link = form.custom_id.data
    if not short_link:
        short_link = get_unique_short_id()
    if not check_short_id_on_unic(short_link):
        flash(f'Имя {short_link} уже занято!', 'link-taken')
        return render_template('urls.html', form=form)
    if not chek_on_sumvols(short_link):
        flash('Указано недопустимое имя для короткой ссылки', 'link-taken')
        return render_template('urls.html', form=form)
    new_url = URLMap(
        original=form.original_link.data,
        short=short_link
    )
    db.session.add(new_url)
    db.session.commit()
    return render_template('urls.html', url=new_url, form=form)


@app.route('/<short_id>')
def follow_link(short_id):
    db_object = URLMap.query.filter_by(short=short_id).first_or_404()
    original_link = db_object.original
    return redirect(original_link)

from flask import render_template, flash, redirect

from yacut import app, db
from .forms import UrlForm
from .models import URLMap
from .const import NOT_CORREKR_BODY_MESSAGE


@app.route('/', methods=['GET', 'POST'])
def index_view():
    url = URLMap()
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('urls.html', form=form)
    short_link = form.custom_id.data
    if not short_link:
        short_link = url.get_unique_short_id()
    if not url.check_short_id_on_unic(short_link):
        flash(f'Имя {short_link} уже занято!', 'link-taken')
        return render_template('urls.html', form=form)
    if not url.chek_on_sumvols(short_link):
        flash(NOT_CORREKR_BODY_MESSAGE, 'link-taken')
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
    db_object = URLMap.get_or_404(short_id)
    original_link = db_object.original
    return redirect(original_link)

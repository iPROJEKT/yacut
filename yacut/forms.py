from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .const import MAX_LEGHT, MIN_LEGHT, PATTERN


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректная ссылка')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(MIN_LEGHT, MAX_LEGHT),
            Regexp(
                regex=PATTERN,
                message='Допустимы только цифры и буквы "a-Z 0-9"'
            )
        ]
    )
    submit = SubmitField('Создать')

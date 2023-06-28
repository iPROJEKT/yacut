from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


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
            Length(1, 16),
            Regexp(
                regex=r'^[a-zA-Z\d]{1,16}$',
                message='Допустимы только цифры и буквы "a-Z 0-9"'
            )
        ]
    )
    submit = SubmitField('Создать')

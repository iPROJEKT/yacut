from string import ascii_letters, digits


EMPTY_BODY_MASSEGE = 'Отсутствует тело запроса'
NOT_CORREKR_BODY_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
URL_IS_NECESSARILY_MESSAGE = '\"url\" является обязательным полем!'

PATTERN = r'^[a-zA-Z\d]{1,16}$'
PATTERN_FOR_GEN_URK = ascii_letters + digits
DICT_LABELS = {
    'original': 'url',
    'short': 'custom_id',
}

MAX_LEGHT = 16
MIN_LEGHT = 1

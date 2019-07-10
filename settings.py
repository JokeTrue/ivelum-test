import re

HABR_LINKS = [
    'https://habrahabr.ru',
    'http://habrahabr.ru',
    'https://habr.com',
    'http://habr.com'
]

HABR_URL_HOST = 'https://habr.com/'

SIX_WORDS_RE = re.compile('(^|[^-\w])([-\w]{6})(?=($|[^-\w]))')

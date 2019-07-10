from views import IndexView

routes = [
    ('GET', '/{url:.*}', IndexView, 'main'),
]

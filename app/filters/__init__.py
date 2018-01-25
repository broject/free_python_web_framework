from .currency_filter import currency_filter


def register_filters(app):
    currency_filter(app)

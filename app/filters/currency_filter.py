class currency_filter(object):
    def __init__(self, app):

        @app.template_filter()
        def to_mn_money(s):
            if s == None:
                s = 0
            return "{:,}".format(int(s)) + "₮"

        app.jinja_env.filters['let_currency'] = to_mn_money

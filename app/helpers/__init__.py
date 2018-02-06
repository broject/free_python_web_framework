from flask_assets import Environment, Bundle


class Helper:
    """
    Helper for global function and assets bundle
    """
    current_app = None

    @classmethod
    def initialize(cls, app):
        cls.current_app = app

        # assets bundle
        Helper._assets_autoload(app)

        # global methods
        Helper._globals_autoload()

    @classmethod
    def register_global(cls, _func):
        cls.current_app.jinja_env.globals[str(_func.__name__)] = _func

    @classmethod
    def register_filter(cls, _func):
        cls.current_app.jinja_env.filters[str(_func.__name__)] = _func

    @staticmethod
    def _globals_autoload():
        import app.helpers.config_helper
        import app.helpers.url_helper
        import app.helpers.date_helper

    @staticmethod
    def _assets_autoload(app):
        assets = Environment(app)
        jss = Bundle(
            Bundle('assets/js/addons/jqextends.min.js'),
            Bundle('assets/js/app.min.js')
        )
        js_all = Bundle(jss, filters='jsmin', output='assets/js/all.js')
        assets.register('js_all', js_all)

        css = Bundle(
            Bundle('assets/css/style.css')
        )
        css_all = Bundle(css, filters='less,cssmin', output='assets/css/all.css')
        assets.register('css_all', css_all)

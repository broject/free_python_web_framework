
# third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# local imports
from .config import app_config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    db.init_app(app)
    migrate = Migrate(app, db)

    csrf = CSRFProtect()
    csrf.init_app(app)
    #login_manager.init_app(app)
    #login_manager.login_message = "You must be logged in to access this page."
    #login_manager.login_view = "auth.login"
    # odo_auth.init_app(app)

    Bootstrap(app)
    
    # Import controllers
    from app.controllers.dashboard import dashboard_controller
    from app.controllers.product.views import product_controller

    # Register blueprint(s)
    app.register_blueprint(dashboard_controller)
    app.register_blueprint(product_controller)

    @app.template_filter('currency')
    def currency_filter(s):
        if s == None:
            s = 0

        return "{:,}".format(int(s)) + "₮"

    app.jinja_env.filters['let_currency'] = currency_filter

    return app

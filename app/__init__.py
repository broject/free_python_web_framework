
# third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_compress import Compress


# Database engine
db = SQLAlchemy()


# Authentication Module
from app.libraries.ho.oauth_lib import oauth_client
oauth_service = oauth_client()


# Web application instance
def create_app(config_name):
    # local imports
    from .config import app_config
    from .filters import register_filters
    from .controllers import register_controllers
    from .helpers import Helper

    # Main module config
    config = app_config[config_name]

    # App module config
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.config.from_pyfile(config.Instance_Config_App)

    db.init_app(app)
    Migrate(app, db)

    csrf = CSRFProtect()
    csrf.init_app(app)

    # Authentication service
    oauth_service.init_app(app)

    Bootstrap(app)
    Compress(app)

    # Register blueprint controllers
    register_controllers(app)

    # Register template filters
    register_filters(app)

    # Register globals
    Helper.initialize(app)

    return app

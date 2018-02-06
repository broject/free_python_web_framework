class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    import os
    Instance_Config_App = 'config.py'
    Instance_Config_Api = 'api_config.py'

    # system info
    CMS_COMPANY = "hiimeloyun llc"
    CMS_TITLE = "MyPy Web CMS"
    CMS_NAME = "MyPy CMS"
    CMS_VERSION = "1.0.0"

    # system base
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = BASE_DIR + "\\static\\uploads"
    ASSETS_DIR = "/static/assets"
    SITE_URL = 'https://localhost:5000/'
    
    # for variables
    MAX_CONTENT_PATH = 2 * 1024 * 1024
    SQLALCHEMY_ECHO = True
    PER_PAGE = 10

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

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
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = BASE_DIR + "\\static\\uploads"
    ASSETS_DIR = "/static/assets"

    CMS_COMPANY = "Odo Ecosystems LLC"
    CMS_TITLE = "Odo Ecosystems"
    CMS_NAME = "ECO CMS"
    CMS_VERSION = "1.0.0"

    DEBUG = True

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

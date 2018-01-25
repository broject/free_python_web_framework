from app.controllers.dashboard import dashboard_controller
from app.controllers.product.views import product_controller


def register_controllers(app):
    app.register_blueprint(dashboard_controller)
    app.register_blueprint(product_controller)

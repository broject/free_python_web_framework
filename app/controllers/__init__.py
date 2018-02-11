from app.controllers.dashboard import dashboard_controller
from app.controllers.company.views import company_controller


def register_controllers(app):
    app.register_blueprint(dashboard_controller)
    app.register_blueprint(company_controller)

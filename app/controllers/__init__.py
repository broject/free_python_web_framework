from app.controllers.dashboard import dashboard
from app.controllers.account.views import account
from app.controllers.company.views import company


def register_controllers(app):
    app.register_blueprint(dashboard)
    app.register_blueprint(account)
    app.register_blueprint(company)

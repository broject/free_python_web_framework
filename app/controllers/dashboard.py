from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for
from app import oauth_service

current_user = None
dashboard = Blueprint('dashboard', __name__, url_prefix='/')


@dashboard.route('/')
# @oauth_service.login_required
def index():
    from app.models.company_models import BranchGoods, BranchPrice
    bg = BranchGoods.get_first()
    bp = BranchPrice.get_first()
    
    par = bp.branchgoods
    child = bg.price

    print('START ************************************')
    print(par)  # <BranchGoods 1 1 1>
    print(child)  # <BranchPrice 1 1500.0 1450.0>
    print('END ************************************')

    return 'hello world'
    # return render_template('dashboard/index.html')

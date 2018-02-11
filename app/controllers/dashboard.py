from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, json
from flask_responses import json_response, xml_response, auto_response

from app import db
from app.models.auth_models import Role, RolePermission
from app.models.company_models import Company, Branch


dashboard_controller = Blueprint('dashboard', __name__, url_prefix='/')


@dashboard_controller.route('/', methods=['GET'])
def index():
    c = Company.get_first()
    customers = c.customers
    print('<<<<<<<<<< RESULT START >>>>>>>>>>')
    print(c.name)
    print('----------------------------------')
    v = []
    for item in customers:
        v.append(item.as_dict())
        print(type(item), '<br>')
    print('<<<<<<<<<< RESULT END >>>>>>>>>>')
    return render_template('dashboard/index.html', data=c, title='Самбар')

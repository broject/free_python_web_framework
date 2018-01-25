from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, json
from flask_responses import json_response, xml_response, auto_response

from app import db
from app.models.product_model import product_model as ProductModel
from app import odo_auth


dashboard_controller = Blueprint('dashboard', __name__, url_prefix='/')


@dashboard_controller.route('/', methods=['GET'])
def index():
    return render_template('dashboard/index.html', title='Самбар')

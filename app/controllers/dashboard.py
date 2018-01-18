from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, json
from flask_responses import json_response, xml_response, auto_response

from app import db
from app.models.product_model import product_model as ProductModel

dashboard_controller = Blueprint('dashboard', __name__, url_prefix='/')


@dashboard_controller.route('/', methods=['GET'])
def dashboard():
    last = ProductModel.get_last()
    last.name = "boroo 3"
    ProductModel.commit(last)
    # if request.args['type'] == 'json':
    products = ProductModel.get_list()
    return jsonify(products=products)
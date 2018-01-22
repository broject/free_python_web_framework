from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, json
from flask_responses import json_response, xml_response, auto_response

from app import db
from app.models.product_model import product_model as ProductModel

dashboard_controller = Blueprint('dashboard', __name__, url_prefix='/')


@dashboard_controller.route('/', methods=['GET'])
def index():
    import uuid

    last = ProductModel.get_first()
    if last is None:
        last = ProductModel()

    last.name = str(uuid.uuid4())
    last.save()

    products = last.get_list()
    return jsonify(products=products)

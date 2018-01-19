from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, json
from flask_responses import json_response, xml_response, auto_response

from app import db
from app.models.product_model import product_model as ProductModel

product_controller = Blueprint('product', __name__, url_prefix='/product')


@product_controller.route('/', methods=['GET'])
def index():
    url = url_for('static', filename='style.css')
    curl = url_for("product.edit", product_id=1)
    return jsonify(url=url, curl=curl)


@product_controller.route('/edit/<int:product_id>', methods=['GET'])
def edit(product_id):
    return jsonify('Editing! ' + str(product_id))

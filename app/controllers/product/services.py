from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, json
from flask_responses import json_response, xml_response, auto_response

from app import db
from app.models.product_model import product_model as ProductModel

product_controller = Blueprint('product', __name__, url_prefix='/api/product')


@product_controller.route('/', methods=['GET'])
def index_GET():
    list = ProductModel.get_list()
    return jsonify(products=list)


@product_controller.route('/edit/<int:product_id>', methods=['GET'])
def edit(product_id):
    return jsonify('Editing! ' + str(product_id))


@product_controller.route('/save', methods=['POST'])
def save(product_id):
    return jsonify('Editing! ' + str(product_id))

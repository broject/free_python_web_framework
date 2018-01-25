from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, json
from flask_responses import json_response, xml_response, auto_response
from flask_paginate import Pagination, get_page_parameter, get_page_args

from app import db
from app.models.product_model import product_model as ProductModel

product_controller = Blueprint('product', __name__, url_prefix='/product')


@product_controller.route('/', methods=['GET'])
def index():
    page, per_page, offset = get_page_args()
    data_count = ProductModel.query.filter_by(deleted=False).count()
    data = ProductModel.query.filter_by(
        deleted=False).limit(per_page).offset(offset)
    search = False
    print('data_count', data_count, per_page, offset)

    pagination = Pagination(page=page, total=data_count, search=search,
                            record_name='', per_page=per_page, css_framework='foundation')

    return render_template('product/index.html',
                           products=data,  pagination=pagination,
                           title='Барааны жагсаалт')


@product_controller.route('/edit/<int:product_id>', methods=['GET'])
def edit(product_id):
    return jsonify('Editing! ' + str(product_id))


@product_controller.route('/save', methods=['POST'])
def save(product_id):
    return jsonify('Saved! ' + str(product_id))

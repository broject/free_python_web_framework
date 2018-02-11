from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, json
from flask_responses import json_response, xml_response, auto_response
from flask_paginate import Pagination, get_page_parameter, get_page_args

from app import db
from app.models.company_models import Company

company_controller = Blueprint('company', __name__, url_prefix='/company')


@company_controller.route('/', methods=['GET'])
def index():
    page, per_page, offset = get_page_args()
    data_count = Company.query.filter_by(deleted=False).count()
    data = Company.query.filter_by(
        deleted=False).limit(per_page).offset(offset)
    search = False
    print('data_count', data_count, per_page, offset)

    pagination = Pagination(page=page, total=data_count, search=search,
                            record_name='', per_page=per_page, css_framework='foundation')

    return render_template('company/index.html',
                           data=data,  pagination=pagination,
                           title='Барааны жагсаалт')


@company_controller.route('/edit/<int:company_id>', methods=['GET'])
def edit(company_id):
    return jsonify('Editing! ' + str(company_id))


@company_controller.route('/save', methods=['POST'])
def save(company_id):
    return jsonify('Saved! ' + str(company_id))

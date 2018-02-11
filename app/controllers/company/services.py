from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, json
from flask_responses import json_response, xml_response, auto_response

from app import db
from app.models.company_models import Company as CompanyModel

company_controller = Blueprint('company', __name__, url_prefix='/api/company')


@company_controller.route('/', methods=['GET'])
def index_GET():
    data = CompanyModel.get_list()
    return jsonify(data=data)


@company_controller.route('/edit/<int:company_id>', methods=['GET'])
def edit(company_id):
    return jsonify('Editing! ' + str(company_id))


@company_controller.route('/save', methods=['POST'])
def save(company_id):
    return jsonify('Editing! ' + str(company_id))

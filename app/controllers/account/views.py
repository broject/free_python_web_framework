from flask import flash, redirect, url_for, render_template, request
from flask_paginate import Pagination, get_page_args

from app import db
from . import account


@account.route('/account/register', methods=['GET', 'POST'])
def register():
    data = []
    return render_template('account/register.html', data=data)
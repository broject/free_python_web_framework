from flask import redirect, url_for, jsonify

from . import auth
from app import oauth_service


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return oauth_service.login()


@auth.route('/get_user', methods=['GET', 'POST'])
def user():
    return jsonify(oauth_service._user_method())


@auth.route('/logout')
def logout():
    oauth_service.logout()
    return redirect(url_for('auth.login'))


@auth.route('/authorized')
def authorized():
    ret = oauth_service.authorized()
    return ret

from flask import redirect, url_for, jsonify

from . import auth
from app import odo_auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return odo_auth.login()


@auth.route('/get_user', methods=['GET', 'POST'])
def user():
    return jsonify(odo_auth._user_method())


@auth.route('/logout')
def logout():
    odo_auth.logout()
    return redirect(url_for('auth.login'))


@auth.route('/authorized')
def authorized():
    ret = odo_auth.authorized()
    return ret

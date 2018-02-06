from flask import Blueprint, Flask, redirect, url_for, session, request, jsonify, abort
from flask_oauthlib.client import OAuth
import json
from collections import namedtuple
from functools import wraps
import logging


class oauth_client:

    def __init__(self):
        pass

    def init_app(self, app):
        self.oauth = OAuth(app)
        remote = self.oauth.remote_app(
            'dev',
            consumer_key='dev',
            consumer_secret='dev',
            request_token_params={'scope': 'email'},
            base_url='http://localhost:8002/api/',
            request_token_url=None,
            access_token_method='POST',
            access_token_url='http://localhost:8002/oauth/token',
            authorize_url='http://localhost:8002/oauth/authorize'
        )

        app.context_processor(self._context_processor)

        @remote.tokengetter
        def get_oauth_token():
            return session.get('dev_token')

        self.remote = remote

    def login(self):
        return self.remote.authorize(callback=url_for('auth.authorized', _external=True))

    def logout(self):
        session.pop('seller_id', None)
        session.pop('dev_token', None)
        session.pop('user', None)

    def authorized(self):
        print('authorized called.')
        # zarim tohioldold ih udaj baina
        ###
        #resp = None
        resp = self.remote.authorized_response()
        ###
        print('authorized called.')

        if resp is None:
            return 'Access denied: error=%s' % (
                request.args['error']
            )
        if isinstance(resp, dict) and 'access_token' in resp:
            session['dev_token'] = (resp['access_token'], '')
            user = self._user_method()
            session['user'] = user
            if user['is_seller'] == 1:
                return redirect(url_for('seller_client.dashboard'))
            elif user['is_buyer'] == 1:
                return redirect(url_for('buyer_client.dashboard'))
            elif user['is_admin'] == 1:
                return redirect(url_for('dashboard.dashboard'))

        return str(resp)

    def _client_method(self):
        ret = self.remote.get("client")
        if ret.status not in (200, 201):
            return abort(ret.status)
        return ret.raw_data

    def _role_method(self):
        ret = self.remote.get("role")
        if ret.status not in (200, 201):
            return abort(ret.status)
        return ret.raw_data

    def _ability_method(self):
        ret = self.remote.get("ability")
        if ret.status not in (200, 201):
            return abort(ret.status)
        return ret.raw_data

    def _user_method(self):
        ret = self.remote.get("user")
        print(ret.status)
        if ret.status not in (200, 201):
            return None

        nt = json.loads(ret.raw_data, object_hook=lambda d: namedtuple(
            'X', d.keys())(*d.values()))
        return nt._asdict()

    def _get_user(self):
        user = session.get('user')
        return user

    def login_required(self, f):
        @wraps(f)
        def inner(*args, **kwargs):
            if not 'dev_token' in session:
                return redirect(url_for('auth.login', next=request.url))

            return f(*args, **kwargs)
        return inner

    def user_is(self, role):
        def callable(f):
            @wraps(f)
            def inner(*args, **kwargs):
                data = self._role_method()
                r = json.loads(data, object_hook=lambda d: namedtuple(
                    'X', d.keys())(*d.values()))
                if r.role != role:
                    return abort(401)

                return f(*args, **kwargs)
            return inner
        return callable

    def user_has(self, ability):
        def callable(f):
            @wraps(f)
            def inner(*args, **kwargs):
                data = self._ability_method()
                a = json.loads(data, object_hook=lambda d: namedtuple(
                    'X', d.keys())(*d.values()))
                if not ability in a.ability:
                    return abort(401)

                return f(*args, **kwargs)
            return inner
        return callable

    def get_oauth_token(self):
        return session.get('dev_token')

    def _context_processor(self):
        user = self._get_user()
        return dict(current_user=user)

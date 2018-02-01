from flask import url_for, jsonify, json, current_app
from app.helpers import Helper
from app.helpers.config_helper import config_item


def site_url(url=None, _external=None):
    if url is not None:
        if _external is not None:
            return url_for(url, _external=_external)
        else:
            return url_for(url)
    else:
        return config_item('SITE_URL')


def static_url(filename):
    filename = filename.strip("/")
    return url_for('static', filename=filename)


def assets_url(filename):
    filename = filename.strip("/")
    return url_for('static', filename='assets/' + filename)


Helper.register_global(site_url)
Helper.register_global(static_url)
Helper.register_global(assets_url)

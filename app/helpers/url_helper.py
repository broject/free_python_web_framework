from flask import url_for, jsonify, json, current_app
from app.helpers import Helper


def static_url(filename):
    filename = filename.strip("/")
    return url_for('static', filename=filename)


Helper.register_global(static_url)


def assets_url(filename):
    filename = filename.strip("/")
    return url_for('static', filename='assets/' + filename)


Helper.register_global(assets_url)

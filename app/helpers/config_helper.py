from flask import url_for, jsonify, json, current_app
from app.helpers import Helper


def config_item(name):
    return current_app.config[name]


Helper.register_global(config_item)

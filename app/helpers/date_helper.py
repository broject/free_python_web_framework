from flask import url_for, jsonify, json
from datetime import datetime
from app.helpers import Helper


def local_datetime(f='%Y-%m-%d %H:%M:%S.%f'):
    d = datetime.now()
    dt = datetime.strptime(str(d), f)
    return (str(dt)[:19])


def utc_datetime(f='%Y-%m-%d %H:%M:%S.%f'):
    d = datetime.utcnow()
    dt = datetime.strptime(str(d), f)
    return (str(dt)[:19])


Helper.register_global(local_datetime)
Helper.register_global(utc_datetime)

from collections import OrderedDict
from flask import json, jsonify
from sqlalchemy import func, text
from sqlalchemy import Boolean, Column, Integer, \
    String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.models import BaseModel


class product_model(BaseModel):
    name = db.Column(db.String(150), index=True)
    barcode = db.Column(db.String(128), index=True, unique=True)
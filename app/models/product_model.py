from collections import OrderedDict
from flask import json, jsonify
from sqlalchemy import func, text
from sqlalchemy import Boolean, Column, Integer, \
    String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.models import BaseModel


class product_model(BaseModel):
    name = db.Column(db.String(100), index=True)
    barcode = db.Column(db.String(255), index=True)

    @classmethod
    def get_list(self):
        product_list = []
        for item in self.query.all():
            product_list.append(item.as_dict())
        return product_list

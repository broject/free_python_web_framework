from collections import OrderedDict
from flask import json, jsonify
from sqlalchemy import func, text
from sqlalchemy import Boolean, Column, Integer, \
    String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr

from app import db


class CoreModel(db.Model):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        cn = cls.__name__
        _i = cn.rfind('_')
        if _i > 0:
            return cn[:_i]
        else:
            return cn

    def as_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


class BaseModel(CoreModel):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, default=db.func.utc_timestamp())
    updated = db.Column(db.TIMESTAMP, default=db.func.utc_timestamp())
    deleted = db.Column(db.Boolean, default=0)

    @classmethod
    def commit(self, obj=None):
        if obj is not None:
            db.session.add(obj)
        db.session.commit()


class product_model(BaseModel):
    name = db.Column(db.String(100), index=True, unique=True)

    @classmethod
    def get_list(self):
        product_list = []
        for item in product_model.query.all():
            product_list.append(item.as_dict())
        return product_list

    @classmethod
    def get_last(self):
        return self.query.order_by(self.id.desc()).first()
        # return product_model.query.filter(product_model.id == db.session.query(
        # func.max(product_model.id))).first()

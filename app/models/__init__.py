from collections import OrderedDict
from flask import json, jsonify

from sqlalchemy import func, text
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr

from app import db


class CoreModel(db.Model):
    __abstract__ = True

    # __tablename__ = name_model as name
    @declared_attr
    def __tablename__(cls):
        cn = cls.__name__.lower()
        _i = cn.rfind('_model')
        if _i > 0:
            return cn[:_i]
        else:
            return cn

    # model as dict
    def as_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result

    def addme(self):
        db.session.add(self)
        return self

    @classmethod
    def commit(self):
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


class BaseModel(CoreModel):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP)
    modified_at = db.Column(db.TIMESTAMP)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def get_first(self):
        return self.query.order_by(self.id.asc()).first()

    @classmethod
    def get_last(self):
        return self.query.order_by(self.id.desc()).first()

    @classmethod
    def get_list_all(self):
        lst = []
        for item in self.query.order_by(self.id.asc()).all():
            lst.append(item.as_dict())
        return lst


class FullBaseModel(BaseModel):
    __abstract__ = True

    created_ip = db.Column(db.String(length=50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    modified_ip = db.Column(db.String(length=50))
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    ordering = db.Column(db.Integer, nullable=False, default=0)

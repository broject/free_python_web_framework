from flask import json, jsonify
from sqlalchemy import func, text
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, \
    Boolean, Integer, String, Text, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from app.models import BaseModel, CoreModel
from datetime import datetime, timedelta


class MediaFolder(BaseModel):
    parent_id = Column(Integer, ForeignKey('mediafolder.id'))
    name = Column(String(150), nullable=False)
    protected = Column(Boolean, nullable=False, default=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<MediaFolder {}>'.format(self.name)


class MediaType(BaseModel):
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<MediaType {} {}>'.format(self.code, self.name)


class Media(BaseModel):
    mediafolder_id = Column(Integer, ForeignKey('mediafolder.id'))
    mediatype_id = Column(Integer, ForeignKey('mediatype.id'))
    title = Column(String(255))
    path = Column(String(1000), nullable=False, default='')
    filename = Column(String(255), nullable=False)
    extension = Column(String(30), nullable=False)
    mimetype = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False, default=0)
    width = Column(Integer, nullable=False, default=0)
    height = Column(Integer, nullable=False, default=0)
    duration = Column(Integer, nullable=False, default=0)
    protected = Column(Boolean, nullable=False, default=False)

    def __init__(self, mediatype_id):
        self.mediatype_id = mediatype_id

    def __repr__(self):
        return '<Media {}>'.format(self.mediatype_id)


class Gender(BaseModel):
    code = Column(String(30), nullable=False, unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<Gender {} {}>'.format(self.code, self.name)


class Unit(BaseModel):
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<Unit {} {}>'.format(self.code, self.name)


class Quality(BaseModel):
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Quality {}>'.format(self.name)


class Business(BaseModel):
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Business {}>'.format(self.name)

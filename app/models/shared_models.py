from flask import json, jsonify
from sqlalchemy import func, text
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, \
    Boolean, Integer, String, Text, Date, DateTime, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from app.models import BaseModel, CoreModel
from datetime import datetime, timedelta


# бүх тохиргоо
class Settings(BaseModel):
    section = Column(String(150), unique=True)
    code = Column(String(150), nullable=False, unique=True)
    name = Column(String(150), nullable=False, unique=True)
    value = Column(Text)

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<Settings {} {}>'.format(self.code, self.name)


# хэрэглэгчийн тодорхойлсон бүс нутаг
class Zone(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    code = Column(String(150), unique=True)
    name = Column(String(150), nullable=False, unique=True)
    data = Column(Text)

    user = relationship('User', backref=backref('Zone', lazy='dynamic'))

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return '<Zone {} {}>'.format(self.user_id, self.name)

    @classmethod
    def allArray(self):
        zones = []
        for n in Zone.query.all():
            zones.append({'id': n.id, 'name': n.name})
        return zones


# нөөцийн файлын сан
class MediaFolder(BaseModel):
    parent_id = Column(Integer, ForeignKey('mediafolder.id'))
    name = Column(String(150), nullable=False)
    protected = Column(Boolean, nullable=False, default=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<MediaFolder {}>'.format(self.name)


# нөөцийн файлуудын төрөл
class MediaType(BaseModel):
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<MediaType {} {}>'.format(self.code, self.name)


# зураг дүрс гэх мэт нөөц файлуудын бүртгэл
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


# хэрэглэгчийн хүйсд ашиглаж болно
class Gender(BaseModel):
    code = Column(String(30), nullable=False, unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<Gender {} {}>'.format(self.code, self.name)


# сав баглаа боодлын төрөл
class Package(BaseModel):
    code = Column(String(150), unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Package {}>'.format(self.name)


# хэмжих нэгүүд бөгөөд барааны тухайд ашигласан
class Unit(BaseModel):
    code = Column(String(30), nullable=False, unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<Unit {} {}>'.format(self.code, self.name)


# юмны чанар бөгөөд бараа бүтээгдэхүүний чанарт ашигласан
class Quality(BaseModel):
    code = Column(String(150), unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Quality {}>'.format(self.name)


# хамрах хүрээг тодорхойлох төрөл бөгөөд компаны аль хэсэгт хамаарахыг заана
class Sphere(BaseModel):
    code = Column(String(150), nullable=False, unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<Sphere {} {}>'.format(self.code, self.name)


# үйл ажиллагааны чиглэл бөгөөд компанид хамааралтай
class Business(BaseModel):
    code = Column(String(150), unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Business {}>'.format(self.name)


# түлхүүр үг гэж ойлгох бөгөөд барааны таг болгон ашигласан
class Tag(BaseModel):
    code = Column(String(150), unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag {}>'.format(self.name)


# хаана ч ашиглаж болох бүх зүйлсийн нэр бөгөөд барааны дитайл бичихэд ашигласан
class Item(BaseModel):
    code = Column(String(150), unique=True)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Item {}>'.format(self.name)

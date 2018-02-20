from flask import json, jsonify
from sqlalchemy import func, text
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, \
    Boolean, Integer, String, Text, Date, DateTime, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.associationproxy import association_proxy

from datetime import datetime, timedelta
from app import db
from app.models import BaseModel, CoreModel
from app.models.shared_models import Media


class Category(BaseModel):
    parent_id = Column(Integer)
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class CategoryTag(CoreModel):
    __tablename__ = 'category_tag'

    category_id = Column(Integer, ForeignKey('category.id'))
    tag_id = Column(Integer, ForeignKey('tag.id'))

    category = relationship("Category", foreign_keys=[category_id])
    tag = relationship("Tag", foreign_keys=[tag_id])

    __table_args__ = (
        PrimaryKeyConstraint('category_id', 'tag_id'),
    )

    def __init__(self, category_id, tag_id):
        self.category_id = category_id
        self.tag_id = tag_id

    def __repr__(self):
        return '<CategoryTag {} {}>'.format(self.category_id, self.tag_id)


class Goods(BaseModel):
    barcode = Column(String(128), nullable=False, unique=True)
    longcode = Column(String(30))
    qrcode = Column(Text)
    name = Column(String(150), nullable=False, unique=True)
    descr = Column(String(500))
    category_id = Column(Integer, ForeignKey('category.id'))
    thumb_id = Column(Integer, ForeignKey('media.id'))
    package_id = Column(Integer, ForeignKey('package.id'))
    # нэгж >>
    # piece_value = 10, piece_unit_id = ширхэг
    # piece_value = 50, piece_unit_id = ширхэг
    piece_unit_id = Column(Integer, ForeignKey('unit.id'))
    piece_value = Column(Float, nullable=False, default=0)
    # жин >>
    # weight_value = 0.5, weight_unit_id = килограмм
    # weight_value = 500, weight_unit_id = грамм
    weight_unit_id = Column(Integer, ForeignKey('unit.id'))
    weight_value = Column(Float, nullable=False, default=0)
    # эзэлхүүн >>
    # cubature_value = 330, cubature_unit_id = миллилитр
    cubature_unit_id = Column(Integer, ForeignKey('unit.id'))
    cubature_value = Column(Float, nullable=False, default=0)
    # үнэ
    particle_price = Column(Float, nullable=False, default=0)
    # бөөний үнэ
    wholesale_price = Column(Float, nullable=False, default=0)
    # бөөний үнийн нөхцөл
    wholesale_cond = Column(String(500))

    category = relationship("Category", foreign_keys=[category_id])
    thumb = relationship("Media", foreign_keys=[thumb_id])
    package = relationship("Package", foreign_keys=[package_id])

    piece_unit = relationship("Unit", foreign_keys=[piece_unit_id])
    weight_unit = relationship("Unit", foreign_keys=[weight_unit_id])
    cubature_unit = relationship("Unit", foreign_keys=[cubature_unit_id])

    def __init__(self, barcode, name):
        self.barcode = barcode
        self.name = name

    def __repr__(self):
        return '<Goods {} {}>'.format(self.barcode, self.name)


class GoodsTag(CoreModel):
    __tablename__ = 'goods_tag'

    goods_id = Column(Integer, ForeignKey('goods.id'))
    tag_id = Column(Integer, ForeignKey('tag.id'))

    goods = relationship("Goods", foreign_keys=[goods_id])
    tag = relationship("Tag", foreign_keys=[tag_id])

    __table_args__ = (
        PrimaryKeyConstraint('goods_id', 'tag_id'),
    )

    def __init__(self, goods_id, tag_id):
        self.goods_id = goods_id
        self.tag_id = tag_id

    def __repr__(self):
        return '<GoodsTag {} {}>'.format(self.goods_id, self.tag_id)


class GoodsCategory(CoreModel):
    __tablename__ = 'goods_category'

    goods_id = Column(Integer, ForeignKey('goods.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    goods = relationship("Goods", foreign_keys=[goods_id])
    category = relationship("Category", foreign_keys=[category_id])

    __table_args__ = (
        PrimaryKeyConstraint('goods_id', 'category_id'),
    )

    def __init__(self, goods_id, category_id):
        self.goods_id = goods_id
        self.category_id = category_id

    def __repr__(self):
        return '<GoodsCategory {} {}>'.format(self.goods_id, self.category_id)


class GoodsDetail(BaseModel):
    __tablename__ = 'goods_detail'

    goods_id = Column(Integer, ForeignKey('goods.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    value = Column(String(255), index=True)
    data = Column(Text)

    def __init__(self, goods_id, item_id):
        self.goods_id = goods_id
        self.item_id = item_id

    def __repr__(self):
        return '<GoodsDetail {} {}>'.format(self.goods_id, self.item_id)


class GoodsMedia(BaseModel):
    __tablename__ = 'goods_media'

    goods_id = Column(Integer, ForeignKey('goods.id'))
    media_id = Column(Integer, ForeignKey('media.id'))
    title = Column(String(255))
    data = Column(Text)

    def __init__(self, goods_id, media_id):
        self.goods_id = goods_id
        self.media_id = media_id

    def __repr__(self):
        return '<GoodsMedia {} {}>'.format(self.goods_id, self.media_id)

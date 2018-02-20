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
from app.models.goods_models import Goods


# салбарын барааны үнийн жагсаалт
class BranchPrice(BaseModel):
    __tablename__ = 'branch_price'

    branchgoods_id = Column(Integer, ForeignKey('branch_goods.id'))
    price = Column(Float, nullable=False, default=0)
    price_cond = Column(String(500))
    wprice = Column(Float, nullable=False, default=0)
    wprice_cond = Column(String(500))
    isdefault = Column(Boolean, nullable=False, default=True)

    branchgoods = relationship("BranchGoods", foreign_keys=[branchgoods_id])

    def __init__(self, branchgoods_id, price=0, wprice=0):
        self.branchgoods_id = branchgoods_id
        self.price = price
        self.wprice = wprice

    def __repr__(self):
        return '<BranchPrice {} {} {}>'.format(self.branchgoods_id, self.price, self.wprice)


# салбарт бүртгэлтэй нийт бараанууд
class BranchGoods(BaseModel):
    __tablename__ = 'branch_goods'

    company_id = Column(Integer, ForeignKey('company.id'))
    branch_id = Column(Integer, ForeignKey('branch.id'))
    goods_id = Column(Integer, ForeignKey('goods.id'))

    company = relationship('Company', foreign_keys=[company_id])
    branch = relationship('Branch', foreign_keys=[branch_id])
    goods = relationship('Goods', foreign_keys=[goods_id])

    # sqlalchemy.exc.InvalidRequestError: On relationship BranchPrice.BranchGoods, 
    # 'dynamic' loaders cannot be used with many-to-one/one-to-one relationships 
    # and/or uselist=False.
    price = relationship("BranchPrice", uselist=False,
                         primaryjoin="and_(BranchGoods.id==branch_price.c.branchgoods_id, "
                         "branch_price.c.isdefault==1)",
                         backref=backref('BranchGoods', uselist=False))

    def __init__(self, company_id, branch_id, goods_id):
        self.company_id = company_id
        self.branch_id = branch_id
        self.goods_id = goods_id

    def __repr__(self):
        return '<BranchGoods {} {} {}>'.format(self.company_id, self.branch_id, self.goods_id)


# *компаний модел
class Company(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    sphere_id = Column(Integer, ForeignKey('sphere.id'))
    business_id = Column(Integer, ForeignKey('business.id'))
    name = Column(String(150), nullable=False, unique=True)
    reg_number = Column(String(50), unique=True)

    user = relationship('User')
    sphere = relationship('Sphere')
    business = relationship('Business')
    branchs = relationship('Branch', back_populates="company")
    # SELECT company_customer.*
    # FROM company_customer, company
    # WHERE company_customer.company_id = %(param_1)s AND company_customer.customer_id = company.id
    customers = relationship('CompanyCustomer',
                             secondary='company_customer', uselist=True,
                             primaryjoin='company_customer.c.company_id==Company.id',
                             secondaryjoin='company_customer.c.customer_id==Company.id',
                             backref=backref('Company', lazy='dynamic'))
    # SELECT company.*
    # FROM company, company_customer
    # WHERE company_customer.company_id = %(param_1)s AND company_customer.customer_id = company.id
    customer_companies = relationship('Company',
                                      secondary='company_customer', uselist=True,
                                      primaryjoin='company_customer.c.company_id==Company.id',
                                      secondaryjoin='company_customer.c.customer_id==Company.id',
                                      backref=backref('Company', lazy='dynamic'))

    def __init__(self, user_id, sphere_id, business_id, name):
        self.user_id = user_id
        self.sphere_id = sphere_id
        self.business_id = business_id
        self.name = name

    def __repr__(self):
        return '<Company {} {} {} {}>'.format(self.user_id, self.sphere_id, self.business_id, self.name)


class CompanyInfo(BaseModel):
    __tablename__ = 'company_info'

    company_id = Column(Integer, ForeignKey('company.id'))
    avatar_id = Column(Integer, ForeignKey('media.id'))
    cover_id = Column(Integer, ForeignKey('media.id'))
    short_name = Column(String(150))
    inter_name = Column(String(150))
    email = Column(String(150))
    phone = Column(String(150))
    fax = Column(String(150))
    weblink = Column(String(1000))
    address = Column(Text)
    overview = Column(Text)
    policy = Column(Text)
    mission = Column(Text)
    vision = Column(Text)
    contents = Column(Text)

    company = relationship('Company')
    avatar = relationship('Media', foreign_keys=[avatar_id])
    cover = relationship('Media', foreign_keys=[cover_id])

    def __init__(self, company_id):
        self.company_id = company_id

    def __repr__(self):
        return '<CompanyInfo {}>'.format(self.company_id)


class Branch(BaseModel):
    company_id = Column(Integer, ForeignKey('company.id'))
    name = Column(String(150), nullable=False, unique=True)
    email = Column(String(150))
    phone = Column(String(150))
    fax = Column(String(150))
    weblink = Column(String(1000))
    address = Column(Text)

    # If you use backref you don't need to declare the relationship on the second table
    company = relationship('Company', back_populates="branchs")

    # SELECT company.id AS company_id,
    # company.created_at AS company_created_at,
    # company.modified_at AS company_modified_at,
    # company.deleted AS company_deleted,
    # company.user_id AS company_user_id,
    # company.business_id AS company_business_id,
    # company.name AS company_name,
    # company.reg_number AS company_reg_number
    # FROM company, branch_customer
    # WHERE branch_customer.branch_id = %(param_1)s AND branch_customer.customer_id = company.id
    customers = relationship('Company',
                             secondary='branch_customer', uselist=True,
                             primaryjoin='branch_customer.c.branch_id==Branch.id',
                             secondaryjoin='branch_customer.c.customer_id==Company.id',
                             backref=backref('Branch', lazy='dynamic'))

    def __init__(self, company_id, name):
        self.company_id = company_id
        self.name = name

    def __repr__(self):
        return '<Branch {} {}>'.format(self.company_id, self.name)


class BranchMember(BaseModel):
    __tablename__ = 'branch_member'

    branch_id = Column(Integer, ForeignKey('branch.id'))
    member_id = Column(Integer, ForeignKey('user.id'))
    role_id = Column(Integer, ForeignKey('role.id'))
    options = Column(Text)

    branch = relationship('Branch')
    member = relationship('User')
    role = relationship('Role')

    def __repr__(self):
        return '<BranchMember {} {} {}>'.format(self.branch_id, self.member_id, self.role_id)


class BranchZone(BaseModel):
    __tablename__ = 'branch_zone'

    branch_id = Column(Integer, ForeignKey('branch.id'))
    zone_id = Column(Integer, ForeignKey('zone.id'))
    options = Column(Text)

    branch = relationship("Branch", foreign_keys=[branch_id])
    zone = relationship("Zone", foreign_keys=[zone_id])

    def __init__(self, branch_id, zone_id):
        self.branch_id = branch_id
        self.zone_id = zone_id

    def __repr__(self):
        return '<BranchZone {} {}>'.format(self.branch_id, self.zone_id)


class CompanyCustomer(BaseModel):
    __tablename__ = 'company_customer'

    company_id = Column(Integer, ForeignKey('company.id'))
    customer_id = Column(Integer, ForeignKey('company.id'))
    options = Column(Text)

    company = relationship("Company", foreign_keys=[company_id])
    customer = relationship("Company", foreign_keys=[customer_id])

    def __init__(self, company_id, customer_id):
        self.company_id = company_id
        self.customer_id = customer_id

    def __repr__(self):
        return '<CompanyCustomer {} {}>'.format(self.company_id, self.customer_id)


class BranchCustomer(CoreModel):
    __tablename__ = 'branch_customer'

    branch_id = Column(Integer, ForeignKey('branch.id'))
    customer_id = Column(Integer, ForeignKey('company.id'))

    branch = relationship("Branch", foreign_keys=[branch_id])
    customer = relationship("Company", foreign_keys=[customer_id])

    __table_args__ = (
        PrimaryKeyConstraint('branch_id', 'customer_id'),
    )

    def __init__(self, branch_id, customer_id):
        self.branch_id = branch_id
        self.customer_id = customer_id

    def __repr__(self):
        return '<BranchCustomer {} {}>'.format(self.branch_id, self.customer_id)

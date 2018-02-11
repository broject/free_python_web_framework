from flask import json, jsonify
from sqlalchemy import func, text
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, \
    Boolean, Integer, String, Text, Date, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.associationproxy import association_proxy

from datetime import datetime, timedelta
from app import db
from app.models import BaseModel, CoreModel
from app.models.media_models import Media


class Company(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    business_id = Column(Integer, ForeignKey('business.id'))
    name = Column(String(150), nullable=False, unique=True)
    reg_number = Column(String(60), nullable=False, unique=True)

    user = relationship('User')
    business = relationship('Business')
    branchs = relationship('Branch', back_populates="company")
    # SELECT company_customer.*
    # FROM company_customer, company
    # WHERE company_customer.company_id = %(param_1)s AND company_customer.customer_id = company.id
    customers = relationship('CompanyCustomer',
                             secondary='company_customer', uselist=True,
                             primaryjoin='company_customer.c.company_id==Company.id',
                             secondaryjoin='company_customer.c.customer_id==Company.id',
                             backref=backref('Company', lazy = 'dynamic'))
    # SELECT company.*
    # FROM company, company_customer
    # WHERE company_customer.company_id = %(param_1)s AND company_customer.customer_id = company.id
    customer_companies = relationship('Company',
                                      secondary='company_customer', uselist=True,
                                      primaryjoin='company_customer.c.company_id==Company.id',
                                      secondaryjoin='company_customer.c.customer_id==Company.id',
                                      backref=backref('Company', lazy = 'dynamic'))

    def __init__(self, user_id, business_id, name, reg_number):
        self.user_id = user_id
        self.business_id = business_id
        self.name = name
        self.reg_number = reg_number

    def __repr__(self):
        return '<Company {} {} {}>'.format(self.business_id, self.reg_number, self.name)


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
    website = Column(String(150))
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
                             backref=backref('Branch', lazy = 'dynamic'))

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

    branch = relationship('Branch')
    member = relationship('User')
    role = relationship('Role')

    def __repr__(self):
        return '<BranchMember {} {} {}>'.format(self.branch_id, self.member_id, self.role_id)


class CompanyCustomer(BaseModel):
    __tablename__ = 'company_customer'

    company_id = Column(Integer, ForeignKey('company.id'))
    customer_id = Column(Integer, ForeignKey('company.id'))
    data = Column(Text)

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

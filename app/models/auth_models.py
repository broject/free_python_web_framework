from flask import json, jsonify
from sqlalchemy import func, text
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, \
    Boolean, Integer, String, Text, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import BaseModel, CoreModel
from datetime import datetime, timedelta


class Role(BaseModel):
    code = Column(Integer, nullable=False, unique=True)
    name = Column(String(150), nullable=False, unique=True)
    title = Column(String(255))

    permissions = relationship('Permission', secondary='role_permission')

    def __init__(self, code, name, title=None):
        self.code = code
        self.name = name.lower()
        self.title = title

    def add_permissions(self, *permissions):
        for permission in permissions:
            existing_permission = Permission.query.filter_by(
                name=permission).first()
            if not existing_permission:
                existing_permission = Permission(permission)
                db.session.add(existing_permission)
                db.session.commit()
            self.permissions.append(existing_permission)

    def remove_permissions(self, *permissions):
        for permission in permissions:
            existing_permission = Permission.query.filter_by(
                name=permission).first()
            if existing_permission and existing_permission in self.permissions:
                self.permissions.remove(existing_permission)

    def __repr__(self):
        return '<Role {}>'.format(self.name)

    def __str__(self):
        return self.name


class Permission(BaseModel):
    name = Column(String(150), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Permission {}>'.format(self.name)

    def __str__(self):
        return self.name


class RolePermission(CoreModel):
    __tablename__ = 'role_permission'

    role_id = Column(Integer, ForeignKey('role.id'))
    permission_id = Column(Integer, ForeignKey('permission.id'))

    role = relationship("Role", foreign_keys=[role_id])
    permission = relationship("Permission", foreign_keys=[permission_id])

    __table_args__ = (
        PrimaryKeyConstraint('role_id', 'permission_id'),
    )

    def __init__(self, role_id, permission_id):
        self.role_id = role_id
        self.permission_id = permission_id

    def __repr__(self):
        return '<RolePermission {} {}>'.format(self.role_id, self.permission_id)

    def __str__(self):
        return self.role_id + ',' + self.permission_id


class User(BaseModel):
    username = Column(String(60), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    phone = Column(String(150))
    password_salt = Column(String(255))
    password_hash = Column(String(255))
    role_id = Column(Integer, ForeignKey('role.id'))
    first_name = Column(String(60))
    last_name = Column(String(60))

    def get_id(self):
        return str(self.id)  # python 3

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @staticmethod
    def check_login(email, password):
        user = User.query.filter_by(email=email).first()
        if user is None:
            return False

        if not user.verify_password(password):
            return False

        return user


class Client(CoreModel):
    # id = Column(db.Integer, primary_key=True)
    # human readable name
    name = Column(String(150))
    client_id = Column(String(50), primary_key=True)
    client_secret = Column(String(255), nullable=False, unique=True)
    client_type = Column(String(50), default='public')
    default_scope = Column(String(500), default='email address')
    redirect_uris = Column(Text)

    def get_redirect_uris(self):
        if self.redirect_uris:
            return self.redirect_uris.split()
        return []

    def get_default_redirect_uri(self):
        v = self.get_redirect_uris()
        if v.amount() > 0:
            return v[0]
        return None

    def get_default_scopes(self):
        if self.default_scope:
            return self.default_scope.split()
        return []

    @property
    def allowed_grant_types(self):
        return ['authorization_code', 'password', 'client_credentials', 'refresh_token']


class Grant(BaseModel):
    user_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'))
    user = relationship('User')

    client_id = Column(String(50), ForeignKey(
        'client.client_id', ondelete='CASCADE'))
    client = relationship('Client')

    code = Column(String(255), nullable=False)
    redirect_uri = Column(String(1000))
    scope = Column(String(500))
    expires = Column(DateTime)

    def get_scopes(self):
        if self.scope:
            return self.scope.split()
        return None


class Token(BaseModel):
    client_id = Column(String(50), ForeignKey(
        'client.client_id', ondelete='CASCADE'))
    client = relationship('Client')

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User')

    token_type = Column(String(50))
    access_token = Column(String(255))
    refresh_token = Column(String(255))
    scope = Column(String(500))
    expires = Column(DateTime)

    def __init__(self, **kwargs):
        expires_in = kwargs.pop('expires_in', None)
        if expires_in is not None:
            self.expires = datetime.utcnow() + timedelta(seconds=expires_in)

        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_scopes(self):
        if self.scope:
            return self.scope.split()
        return []

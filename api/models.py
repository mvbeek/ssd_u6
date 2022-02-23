'''
This Python file takes care of models that contain the following:
    - User
    - Role
    - UserRoles
    - Report

Also Marshmallow is used to serialize and deserialize the models.
By this library, we can easily create a JSON object from the models.
'''

from datetime import datetime
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.conf.database import Base


class RolesUsers(Base):
    '''
    RolesUsers class that contains the relationship between User and Role.
    '''
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(Base, RoleMixin):
    '''
    Role class that contains the Role information.
    '''
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base, UserMixin):
    '''
    User class that contains the User information, including:
        - id
        - email
        - username
        - password
        - last_login_at
        - current_login_at
        - last_login_ip
        - current_login_ip
        - login_count
        - active
        - fs_uniquifier
            : unique identifier for the user, mainly used for token
        - confirmed_at
        - roles
    '''
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime(), default=datetime.now)
    current_login_at = Column(DateTime(), default=datetime.now)
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))


class Report(Base):
    '''
    Report class that contains the Report information, including:
        - id
        - user_id
        - name
        - description
        - created_at
        - updated_at
        - url
        - file_name
    '''
    __tablename__ = 'report'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(),
                        default=datetime.now,
                        onupdate=datetime.now)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('reports', lazy='dynamic'))
    url = Column(String(255))
    file_name = Column(String(255))


class ReportSchema(SQLAlchemyAutoSchema):
    '''
    ReportSchema class for serializing the Report model.
    '''
    class Meta:
        '''
        configuration of the ReportSchema class.
        '''
        model = Report
        include_relationships = True
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    '''
    UserSchema class for serializing the User model.
    '''
    class Meta:
        '''
        configuration of the UserSchema class.
        '''
        model = User
        include_relationships = True
        load_instance = True

#!/usr/bin/env python3
"""
    database - user.py
    Author: Daryl Stark

    Table for users
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Database
import datetime
#---------------------------------------------------------------------------------------------------
class User(Database.base_class):
    """ Table for users """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'users'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('fullname'),
        UniqueConstraint('username'),
        UniqueConstraint('password_salt')
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    created =       Column(DateTime, nullable = False, default = datetime.datetime.utcnow)
    fullname =      Column(String(128), nullable = False)
    username =      Column(String(128), nullable = False)
    password =      Column(String(128), nullable = False)
    password_salt = Column(String(128), nullable = False)

    # One-to-many relationship mappings
    user_api_tokens = relationship("APIUserToken")

    # Fields that need to be hidden from the API
    api_hide_fields = [ 'password', 'password_salt' ]
#---------------------------------------------------------------------------------------------------
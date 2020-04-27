#!/usr/bin/env python3
"""
    database - user.py
    Author: Daryl Stark

    Table for users
"""
#---------------------------------------------------------------------------------------------------
# Imports
import sqlalchemy
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from database import Database
from passlib.hash import argon2
import datetime
import pyotp
#---------------------------------------------------------------------------------------------------
class User(Database.base_class):
    """ Table for users """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'users'

    # The object-type for the output of the API
    __objecttype__ = 'user'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('username'),
        UniqueConstraint('email')
    )

    # Database columns for this table
    id =                Column(Integer, primary_key = True)
    created =           Column(DateTime, nullable = False, default = datetime.datetime.utcnow)
    fullname =          Column(String(128), nullable = False)
    username =          Column(String(128), nullable = False)
    email =             Column(String(128), nullable = False)
    password =          Column(String(512), nullable = False)
    password_date =     Column(DateTime, nullable = False)
    secret =            Column(String(256), nullable = True)
    secret_verified =   Column(Boolean, nullable = False, default = True)

    # One-to-many relationship mappings
    user_api_tokens = relationship("APIUserToken")

    # Fields that need to be hidden from the API
    api_hide_fields = [ 'password', 'secret' ]
    api_extra_fields = [ 'second_factor_enabled' ]

    def set_password(self, password):
        """ Method to set the password for this user """
        self.password = argon2.hash(password)
        self.password_date = datetime.datetime.utcnow()
    
    def verify_password(self, password):
        """ Checks the password and returns True if the given password is correct """
        return argon2.verify(password, self.password)
    
    def generate_secret(self):
        """ Method to generate a random secret for this object. The secret gets returned so the
            client can present this to the user """
        self.secret = pyotp.random_base32()
        self.secret_verified = False
        return self.secret

    @property
    def second_factor_enabled(self):
        """ Property that returns of a secret is filled in """
        return not self.secret is None and self.secret_verified
#---------------------------------------------------------------------------------------------------
#!/usr/bin/env python3
""",
    database - api_user_token.py
    Author: Daryl Stark

    Table for APIUserToken objects. A user token is a token that an application can use to identify
    run APIs as a specific user. This way, the application doesn't have to know the user
    credentials, but still can run things on behalf of the user.

    The description can be used by the user to describe this user token. If the token is used for
    a login session to a webinterface, for example, he can use this field to note the device on
    which this session is create (like 'Work laptop')
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Database
import datetime
#---------------------------------------------------------------------------------------------------
class APIUserToken(Database.base_class):
    """ Table for API user tokens """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_user_tokens'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('token'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    user =          Column(ForeignKey("users.id"), nullable = False)
    client_token =  Column(ForeignKey("api_client_tokens.id"), nullable = False)
    created =       Column(DateTime, nullable = False, default = datetime.datetime.utcnow)
    expiration =    Column(DateTime, nullable = True)
    enabled =       Column(Boolean, nullable = False, default = False)
    token =         Column(String(64), nullable = False)
    description =   Column(String(64), nullable = True)

    # One-to-many relationship mappings
    users_permissions = relationship("APIUserPermission")

    # Many-to-one relationship mappings
    client = relationship("APIClientToken")
#---------------------------------------------------------------------------------------------------

#!/usr/bin/env python3
""",
    database - api_client_token.py
    Author: Daryl Stark

    Table for APIClientToken objects. A client token is a token that an client can use to identify
    itself to the API. As soon as it is authenticated, it still needs to be authorized at everything
    it does. We do this with certain API permissions.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Database
import datetime
import string
import random
#---------------------------------------------------------------------------------------------------
class APIClientToken(Database.base_class):
    """ Table for API client tokens """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_client_tokens'

    # The object-type for the output of the API
    __objecttype__ = 'api_client_token'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('token'),
        UniqueConstraint('app_name', 'app_version'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    created =       Column(DateTime, nullable = False, default = datetime.datetime.utcnow)
    expiration =    Column(DateTime, nullable = True)
    enabled =       Column(Boolean, nullable = False, default = False)
    app_name =      Column(String(128), nullable = False)
    app_version =   Column(String(128), nullable = False)
    app_publisher = Column(String(128), nullable = False)
    token =         Column(String(64), nullable = False)

    # One-to-many relationship mappings
    user_api_tokens = relationship("APIUserToken")
    client_permissions = relationship("APIClientPermission")

    def generate_random_token(self):
        """ Method to generate a random client token """

        # Characters for the random key
        characters = string.ascii_lowercase + string.digits

        # Create the token and set it
        self.token = ''.join(random.choice(characters) for x in range(32))
#---------------------------------------------------------------------------------------------------

#!/usr/bin/env python3
""",
    database - api_client_permission.py
    Author: Daryl Stark

    Table for APIClientPermission objects. This table contains the permissions for the APIClientKeys
    objects. As soon as a client authenticates with a APIClientToken, these permissions authorize
    certain actions.

    The 'granted' column is either True or False; True meaning the permission is granted and the
    API Client can do whatever is to be done with this permission. False means the key doesn't have
    the correct permission.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Database
#---------------------------------------------------------------------------------------------------
class APIClientPermission(Database.base_class):
    """ Table for API permissions for Client tokens """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_client_permissions'

    # The object-type for the output of the API
    __objecttype__ = 'api_client_permissions'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('client_token', 'permission'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    client_token =  Column(ForeignKey("api_client_tokens.id"), nullable = False)
    permission =    Column(ForeignKey("api_permissions.id"), nullable = False)
    granted =       Column(Boolean, nullable = False)

    # Many-to-one relationship mappings
    permission_object = relationship("APIPermission")
#---------------------------------------------------------------------------------------------------
#!/usr/bin/env python3
""",
    database - api_user_permission.py
    Author: Daryl Stark

    Table for APIUserPermission objects. This table contains the permissions for the APIUserKeys
    objects. As soon as a client authenticates with a APIUserToken, these permissions authorize
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
class APIUserPermission(Database.base_class):
    """ Table for API permissions for User tokens """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_user_permissions'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('user_token', 'permission'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    user_token =    Column(ForeignKey("api_user_tokens.id"), nullable = False)
    permission =    Column(ForeignKey("api_permissions.id"), nullable = False)
    granted =       Column(Boolean, nullable = False)
#---------------------------------------------------------------------------------------------------
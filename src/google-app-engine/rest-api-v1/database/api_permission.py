#!/usr/bin/env python3
""",
    database - api_permission.py
    Author: Daryl Stark

    Table for APIPermission objects. This table only contains the possible permissions that exists.
    In seperate tables, permissions are granted to application keys and user keys. Each permissions
    has two parts; the section and the subject. A API endpoint can check if the correct permissions
    are given to the requester based on these two values.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Database
#---------------------------------------------------------------------------------------------------
class APIPermission(Database.base_class):
    """ Table for API permissions """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_permissions'

    # Set constrains for this table
    __table_args__ = (
        UniqueConstraint('section', 'subject'),
    )

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    section =       Column(String(128), nullable = False)
    subject =       Column(String(128), nullable = False)
    description =   Column(String(512), nullable = False)

    # One-to-many relationship mappings
    user_permissions = relationship("APIUserPermission")
    client_permissions = relationship("APIClientPermission")
#---------------------------------------------------------------------------------------------------
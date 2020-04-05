#!/usr/bin/env python3
""",
    database - api_user_logentry.py
    Author: Daryl Stark

    Table for APIUserLogEntry's objects. When a user does something, a object of this class is
    added to the database as a kind of logging. This way, a audit trail can be compiled.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Database
import datetime
#---------------------------------------------------------------------------------------------------
class APIUserLogEntry(Database.base_class):
    """ Table for API user accounting logs """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_user_log'

    # The object-type for the output of the API
    __objecttype__ = 'api_user_logentry'

    # Database columns for this table
    id =                    Column(Integer, primary_key = True)
    datetime =              Column(DateTime, nullable = False, default = datetime.datetime.utcnow)
    user =                  Column(ForeignKey("api_user_tokens.id"), nullable = False)
    method =                Column(String(16), nullable = False)
    api_group =             Column(String(32), nullable = False)
    api_endpoint =          Column(String(32), nullable = False)
    permission =            Column(ForeignKey("api_permissions.id"), nullable = False)

    # Many-to-one relationship mappings
    permission_object = relationship("APIPermission")
    api_user_object = relationship("APIUserToken")
#---------------------------------------------------------------------------------------------------

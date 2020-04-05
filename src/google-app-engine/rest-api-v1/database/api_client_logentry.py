#!/usr/bin/env python3
""",
    database - api_client_logentry.py
    Author: Daryl Stark

    Table for APIClientLogEntry's objects. When a client does something, a object of this class is
    added to the database as a kind of logging. This way, a audit trail can be compiled.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Database
import datetime
#---------------------------------------------------------------------------------------------------
class APIClientLogEntry(Database.base_class):
    """ Table for API client accounting logs """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'api_client_log'

    # The object-type for the output of the API
    __objecttype__ = 'api_client_logentry'

    # Database columns for this table
    id =                    Column(Integer, primary_key = True)
    datetime =              Column(DateTime, nullable = False, default = datetime.datetime.utcnow)
    address =               Column(String(48), nullable = False)
    client =                Column(ForeignKey("api_client_tokens.id"), nullable = False)
    method =                Column(String(16), nullable = False)
    api_group =             Column(String(32), nullable = False)
    api_endpoint =          Column(String(32), nullable = False)
    permission =            Column(ForeignKey("api_permissions.id"), nullable = False)

    # Many-to-one relationship mappings
    permission_object = relationship("APIPermission")
    api_client_object = relationship("APIClientToken")
#---------------------------------------------------------------------------------------------------

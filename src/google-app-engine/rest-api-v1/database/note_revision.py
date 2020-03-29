#!/usr/bin/env python3
""",
    database - note_revision.py
    Author: Daryl Stark

    Table for NoteRevision objects
"""
#---------------------------------------------------------------------------------------------------
# Imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Database
import datetime
#---------------------------------------------------------------------------------------------------
class NoteRevision(Database.base_class):
    """ Table for note-revisions """

    # Mandatory argument for Database objects within SQLAlchemy
    __tablename__ = 'note_revisions'

    # Database columns for this table
    id =            Column(Integer, primary_key = True)
    created =       Column(DateTime, nullable = False, default = datetime.datetime.utcnow)
    note =          Column(ForeignKey("notes.id"), nullable = False)
    text =          Column(String(16777216), nullable = False)
#---------------------------------------------------------------------------------------------------
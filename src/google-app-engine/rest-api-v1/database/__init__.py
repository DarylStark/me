"""
    Package: database
    __init__.py
    
    Initiator for the 'database' package. Imports all the classes from the package so this
    package can be used as a package
"""
#---------------------------------------------------------------------------------------------------
# Main class: Database
from database.database import Database

# Session manager
from database.database_session import DatabaseSession

# Tables
#from database.note_revision import NoteRevision
#from database.note import Note
from database.user import User
#---------------------------------------------------------------------------------------------------
#!/usr/bin/env python3
"""
    database - database_session.py

    Class for database sessions. Can be used as context manager
"""
#---------------------------------------------------------------------------------------------------
# Imports
from database import Database
#---------------------------------------------------------------------------------------------------
class DatabaseSession:
    """ Class for database session. Can and should be used as context manager """

    def __init__(self, commit_on_end = False, expire_on_commit = True):
        """ The initiator creates an empty session to use with this object. When 'expire_on_commit'
            is set, all objects that were added during this session are expired after the session is
            commited """

        self.session = Database.session(expire_on_commit = expire_on_commit)
        self.commit_on_end = commit_on_end
    
    def close(self):
        """ Closes the session """
        self.session.close()
    
    def commit(self):
        """ Commits the session """
        self.session.commit()
    
    def rollback(self):
        """ Rolls back the session """
        self.session.rollback()
    
    def __enter__(self, ):
        """ Context manager for the session. Makes sure you can use the session as Context Manager
            and prevents errors """
        return self.session
    
    def __exit__(self, type, value, traceback):
        """ The end of the context manager. Commits the session (if the user requested this) and
            closes the session """
        
        # Commit, if needed
        if self.commit_on_end:
            self.commit()
        
        # Close the session
        self.close()

        # If 'type' is None, there was no error so we can return True. Otherwise, False is returned
        # and the exception is passed through
        return type is None
#---------------------------------------------------------------------------------------------------
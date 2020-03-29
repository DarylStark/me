"""
    database - exceptions
    Author: Daryl Stark

    Module with custom exceptions for 'database'
"""
#---------------------------------------------------------------------------------------------------
# Bases classes for Exceptions
#---------------------------------------------------------------------------------------------------
class DatabaseError(Exception):
    """ Base exception for Database-exceptions """
    pass
#---------------------------------------------------------------------------------------------------
class DatabaseCriticalError(DatabaseError):
    """ Exception that should result in complete termination of the application """
    pass
#---------------------------------------------------------------------------------------------------
# Critical errors; errors that should stop the complete application
#---------------------------------------------------------------------------------------------------
class DatabaseConnectionError(DatabaseCriticalError):
    """ Error that happends when the database credentials are not correct """
    pass
#---------------------------------------------------------------------------------------------------
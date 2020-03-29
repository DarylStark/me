#!/usr/bin/env python3
"""
    database - database
    Author: Daryl Stark

    Main class for the Database object. Will be an static class that cannot be initiated.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from database.exceptions import DatabaseConnectionError
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#---------------------------------------------------------------------------------------------------
class Database():
    """ Main class for the Database object. Will be an static class that cannot be initiated. """
    
    _engine = None
    base_class = declarative_base()
    session = sessionmaker()

    # Methods to make sure this class is used as it is suppoes to be
    def __new__(cls):
        """ When someone tries to create a instance of it, we give an error """
        raise TypeError('It is impossible to create a instance of class "{classname}"'.format(
            classname = cls.__name__
        ))

    @classmethod
    def connect(cls, connection, echo = False, pool_pre_ping = True, pool_recycle = 10, pool_size = 5, pool_overflow = 10):
        """ Method to create a SQLAlchemy engine. Uses the database and credentials given by the
            user. Since this is a static class, we set it in the class parameter. This way, the
            complete application uses the same database engine. After creating the engine, it calls
            the command to create the tables in the database. 
            
            This method has a few parameters for creating the engine:
            - echo:          Can be used for debugging; writes the queries for SQLAlchemy to the
                             stdout buffer
            - pool_pre_ping: By default True. Determines if SQLAlchemy should do a pre-check before
                             using a connection that is already in the pool. By doing this, we can
                             prevent it from using dead connections
            - pool_recycle:  After how many seconds SQLAlchemy considers a MySQL connection to be
                             stale and therefore removed from the database
            - pool_size:     The size the pool can get
            - pool_overflow: How many connections SQLAlchemy can go over the pool_size
        """
        
        try:
            # Create the engine
            cls._engine = create_engine(
                connection,
                echo = echo,
                pool_pre_ping = pool_pre_ping,
                pool_recycle = pool_recycle,
                pool_size = pool_size,
                max_overflow = pool_overflow
            )

            # Create the configured tables
            cls.base_class.metadata.create_all(cls._engine)

            # Bind the engine to the sessionmaker of the class
            cls.session.configure(bind = cls._engine)
        except sqlalchemy.exc.OperationalError:
            raise DatabaseConnectionError('Couldn\'t connect to database')
#---------------------------------------------------------------------------------------------------

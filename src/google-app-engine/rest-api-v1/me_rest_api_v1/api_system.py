#!/usr/bin/env python3
"""
    me_rest_api_v1 - api_system.py

    API module for '/system'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me_rest_api_v1 import MeRESTAPIv1
from me_rest_api_v1 import APIResponse
from me_rest_api_v1.exceptions import *
from database import Database
import os
from psutil import Process
#---------------------------------------------------------------------------------------------------
@MeRESTAPIv1.register_group(name = 'system', description = 'Authentication and authorization')
class APISystem:
    """ API class for 'system'. Can be used to retrieve system information """

    @MeRESTAPIv1.register_endpoint(
        group = 'system',
        name = 'retrieve_info',
        description = 'Retrieve system information',
        permissions = {
            'GET': 'system.retrieve_info'
        },
        user_token_needed = False
    )
    def retrieve_info(*args, **kwargs):
        """ Endpoint for clients to retrieve system information """
        
        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_RECORD)

        # Get the process ID (pid) and create a PSUtil Process object of it. We can use this later
        # to get specific information about the process
        pid = os.getpid()
        process = Process(pid)

        # Get information about the process
        process = {
            'pid': pid,
            'used_memory': process.memory_info().rss,
            'cpu_percentage': process.cpu_percent()
        }

        # Get information about the application
        application = {
            'environment': MeRESTAPIv1.environment
        }

        # Get information about the database
        # TODO: Make a property in the Database class for this instead of using the hidden variable
        database = {
            'pool_size': Database._engine.pool.size(),
            'checked_in': Database._engine.pool.checkedin(),
            'overflow': Database._engine.pool.overflow(),
            'checked_out': Database._engine.pool.checkedout()
        }

        # Set the object in the response
        response.data = {
            'process': process,
            'application': application,
            'database': database
        }

        return response
#---------------------------------------------------------------------------------------------------
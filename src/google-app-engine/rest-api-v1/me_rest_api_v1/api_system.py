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
        user_token_needed = False,
        documentation = {
            'GET': {
                'description': 'Returns information about the API system',
                'data': 'This endpoint doesn\'t require any data',
                'return': 'Returns a JSON object with system information: process information, application information and database'
            }
        }
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
            'environment': MeRESTAPIv1.environment,
            'starttime': MeRESTAPIv1.starttime
        }

        # Get information about the database
        database = Database.get_pool_statistics()

        # Set the object in the response
        response.data = {
            'process': process,
            'application': application,
            'database': database
        }

        return response
#---------------------------------------------------------------------------------------------------
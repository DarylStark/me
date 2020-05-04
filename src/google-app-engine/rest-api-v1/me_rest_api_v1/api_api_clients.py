#!/usr/bin/env python3
"""
    me_rest_api_v1 - api_api_clients.py

    API module for '/api_clients'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from flask import request
from me_rest_api_v1 import MeRESTAPIv1
from me_rest_api_v1 import APIResponse
from me_rest_api_v1.exceptions import *
from database import DatabaseSession
from database import APIClientToken
#---------------------------------------------------------------------------------------------------
@MeRESTAPIv1.register_group(name = 'api_clients', description = 'API Client management')
class APIAPIClients:
    """ API class for 'api_clients'. Can be used to manage API clients """

    @MeRESTAPIv1.register_endpoint(
        group = 'api_clients',
        name = 'client',
        description = 'Create, retrieve, update or delete API Client tokens',
        permissions = {
            'GET': 'api_clients.retrieve_clients'
        },
        user_token_needed = True
    )
    def client(*args, **kwargs):
        """ Endpoint for users to create, retrieve, update or delete API client tokens """

        if request.method.upper() == 'GET':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_DATASET)
            
            # Get all permissions from the database
            with DatabaseSession() as session:
                # Get the client tokens
                client_tokens = session.query(APIClientToken)
            
            # Set the return data
            response.data = client_tokens.all()

            # Return the object
            return response
#---------------------------------------------------------------------------------------------------
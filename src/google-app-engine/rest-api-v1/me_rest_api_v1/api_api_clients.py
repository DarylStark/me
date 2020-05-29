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
            'GET': 'api_clients.retrieve_client_token',
            'PATCH': 'api_clients.update_client_token'
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
        
        if request.method.upper() == 'PATCH':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_DONE)

            # Get the given data
            json_data = request.json

            # Check if we got an 'id'
            if not 'id' in json_data.keys():
                raise MeRESTAPIv1APIClientUpdateClientTokenMissingIDError('Missing "id" in data')
            
            # Get all permissions from the database
            with DatabaseSession(commit_on_end = True) as session:
                # Get the client tokens
                client_tokens = session.query(APIClientToken).filter(APIClientToken.id == json_data['id'])

                # Check if we got an token
                if client_tokens.count() != 1:
                    raise MeRESTAPIv1APIClientUpdateClientTokenNotFoundError(f'Client token with id {json_data["id"]} cannot be found')
                
                # Get the token object
                token_object = client_tokens.first()
                
                # Update the 'enabled' field
                if 'enabled' in json_data.keys():
                    token_object.enabled = json_data['enabled']
            
            # Return the response
            response.data = True
            return response
#---------------------------------------------------------------------------------------------------
#!/usr/bin/env python3
"""
    me_rest_api_v1 - api_search.py

    API module for '/search'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from flask import request
from me_rest_api_v1 import MeRESTAPIv1
from me_rest_api_v1 import APIResponse
from me_rest_api_v1.exceptions import *
from database import DatabaseSession
from database import APIUserToken
from database import APIClientToken
from sqlalchemy import or_
from sqlalchemy import and_
#---------------------------------------------------------------------------------------------------
@MeRESTAPIv1.register_group(name = 'search', description = 'Search for resources')
class APISearch:
    """ API class for 'search'. Can be used to search for resources """

    @MeRESTAPIv1.register_endpoint(
        group = 'search',
        name = 'search',
        description = 'Search for system resources',
        permissions = {
            'GET': 'search.search'
        },
        user_token_needed = True,
        documentation = {
            'GET': {
                'description': 'Search for system resources',
                'data': 'A argument with the name "query" is required and represents the search query',
                'return': 'Returns a JSON list with found objects that the user has permissions to'
            }
        }
    )
    def search(*args, **kwargs):
        """ Endpoint for clients to retrieve system information """
        
        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_DATASET)

        # Check if we got a query
        if not request.args.get('query'):
            raise MeRESTAPIv1SearchNoQuerySpecifiedError('No "query" specified')

        # Save the query
        query = request.args.get('query')

        # Get the client token and the user token
        client_token = kwargs['client_token']
        user_token = kwargs['user_token']

        # Get the permissions for the tokens
        client_permissions = MeRESTAPIv1.get_token_permissions('client', client_token)
        user_permissions = MeRESTAPIv1.get_token_permissions('user', user_token)
        permissions = set(client_permissions + user_permissions)

        # Create a empty list. During the searches we will add items to this list and eventually,
        # this list will be returned
        results = list()

        # Create a DatabaseSession for all the searches
        with DatabaseSession() as session:
            # Get the current user. We need this later to make sure we only find resources that the
            # user created
            user_id = session.query(APIUserToken).filter(APIUserToken.token == user_token).first().user

            # Search through the client tokens
            if 'api_clients.retrieve_client_permissions' in permissions:
                resources = session.query(APIClientToken).filter(or_(
                    APIClientToken.app_name.ilike(f'%{query}%'),
                    APIClientToken.app_publisher.ilike(f'%{query}%')
                )).all()

                # Add them to the result
                results += resources
            
            # Search through the user tokens
            if 'aaa.retrieve_user_token' in permissions:
                resources = session.query(APIUserToken).filter(and_(
                    APIUserToken.description.ilike(f'%{query}%'),
                    APIUserToken.user == user_id
                )).all()

                # Add them to the result
                results += resources

        # Set the database
        response.data = results

        # Return the resources
        return response
#---------------------------------------------------------------------------------------------------
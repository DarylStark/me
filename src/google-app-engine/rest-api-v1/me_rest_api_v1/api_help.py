#!/usr/bin/env python3
"""
    me_rest_api_v1 - api_help.py

    API module for '/help'
"""
#---------------------------------------------------------------------------------------------------
# Imports
import re
from me_rest_api_v1 import MeRESTAPIv1
from me_rest_api_v1 import APIResponse
from me_rest_api_v1.exceptions import *
#---------------------------------------------------------------------------------------------------
@MeRESTAPIv1.register_group(name = 'help', description = 'Description of the API endpoints')
class APIHelp:
    """ API class for 'help'. Can be used to retrieve API help """
    
    @MeRESTAPIv1.register_endpoint(
        group = 'help',
        name = 'endpoints',
        description = 'Retrieve all API endpoints',
        permissions = {
            'GET': 'help.retrieve_endpoints'
        },
        user_token_needed = True,
        documentation = {
            'GET': {
                'description': 'Returns the API groups and their endpoints, including a description, needed permissions per method and documentation',
                'data': 'This endpoint doesn\'t require any data',
                'return': 'Returns a list of API groups. Each group contains a list of associated API endpoints which contain a list of supported methods'
            }
        }
    )
    def retrieve_endpoints(*args, **kwargs):
        """ API endpoint to retrieve the API groups and API endpoints """

        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_DATASET)

        # Create a empty dataset
        dataset = list()

        # Add the groups and endpoints to the dataset
        for group, item in MeRESTAPIv1.registered_groups.items():
            # Create a help item
            group = {
                '_type': 'api_group',
                'name': group,
                'description': item['description'],
                'endpoints': list()
            }

            # Add the endpoints
            for endpoint, item_endpoint in item['endpoints'].items():
                # Create a endpoint item
                endpoint = {
                    '_type': 'api_endpoint',
                    'name': endpoint,
                    'description': item_endpoint['description'],
                    'documentation': item_endpoint['documentation'],
                    'permissions': item_endpoint['permissions'],
                    'user_token_needed': item_endpoint['user_token_needed']
                }

                # Add it to the 'endpoints' item of the group
                group['endpoints'].append(endpoint)

            # Add it to the dataset
            dataset.append(group)

        # Get the API endpoints
        response.data = dataset

        # Return the response
        return response
#---------------------------------------------------------------------------------------------------

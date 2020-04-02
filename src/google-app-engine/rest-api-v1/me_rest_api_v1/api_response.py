#!/usr/bin/env python3
"""
    me_rest_api_v1 - api_response.py

    Class that represents a API response
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me_rest_api_v1.exceptions import *
from time import time
import math
#---------------------------------------------------------------------------------------------------
class APIResponse:
    """ API class that represents a API response """

    # The response types that exist
    TYPE_DATASET = 1    # For APIs that return lists of data
    TYPE_RECORD = 2     # For APIs that create or modify data and return the new or modified object
    TYPE_DONE = 3       # For APIs that respond when something is done, like remving a object

    def __init__(self, response_type = None):
        """ The initiator sets default values """

        # Set the API endpoint characteristics. These are typically set by the decorator for the
        # callback
        self.api_group = None
        self.api_endpoint = None

        # Set the timing. Also set by the decorator
        self.starttime = None
    
        # Type APIResponse type. This one is set by the endpoint itself and specifies what kind of
        # response this is. Should always be set
        self.response_type = response_type

        # The data that the endpoint returns. Should be set by the endpoint itself
        self.data = None

        # Paginating. If the 'paginate' option is set to True, the decorator will do the paginating.
        # A endpoint can choose to do this self by setting this option to False. This can be usefull
        # for endpoints that handle a lot of data.
        self.paginate = True
        self.page = None
        self.items_per_page = None
        self.last_page = None
        self.item_count = None
        self.all_item_count = None
    
    @property
    def response(self):
        """ Property to return the object itself as a dict """

        # Check if a valid type is set
        if not self.response_type in (APIResponse.TYPE_DATASET, APIResponse.TYPE_RECORD, APIResponse.TYPE_DONE):
            raise MeRESTAPIv1EndpointWrongResponseTypeError('Response type {response_type} is not valid'.format(
                response_type = return_object.response_type
            ))

        # Create the default response dictionary
        response_dict = {
            'request': {
                'group': self.api_group,
                'endpoint': self.api_endpoint
            },
            'response': {
                'type': self.response_type,
                'runtime': round(time() - self.starttime, 3)
            }
        }

        # If this is dataset, we have to add the data
        if self.response_type == self.TYPE_DATASET:
            # Check if the data is a list
            if not type(self.data) is list:
                raise MeRESTAPIv1EndpointDataNotAListError('Data is of type "{bad_type} and not of type "{good_type}"'.format(
                    bad_type = type(self.data),
                    good_type = list
                ))
            
            # Do paginating, if needed
            if self.paginate:
                # Calulcate what the last page should be
                self.all_item_count = len(self.data)
                self.last_page = int(math.ceil(self.all_item_count / self.items_per_page))

                # Sanatize the page
                if self.page > self.last_page or self.page < 1:
                    raise MeRESTAPIv1EndpointInvalidPageError('The page {page} should be between 1 and {max_page}'.format(
                        page = self.page,
                        max_page = self.last_page
                    ))
                
                # Slice the data
                start = (self.page - 1) * self.items_per_page
                self.data = self.data[start:self.items_per_page + start]

            # Add the data
            response_dict['dataset'] = {
                'data': self.data,
                'page': self.page,
                'items_per_page': self.items_per_page,
                'last_page': self.last_page,
                'item_count': len(self.data),
                'all_item_count': self.all_item_count
            }
        
        # If this is dataset, we have to add the data
        if self.response_type == self.TYPE_RECORD:
            # If we only have one record to return, we set it in the data
            response_dict['object'] = self.data
        
        # If this is done-thingy, we check if data is a boolean and if it is, we set that as the
        # return type
        if self.response_type == self.TYPE_DONE:
            if type(self.data) is bool:
                response_dict['progress'] = self.data
            else:
                raise MeRESTAPIv1EndpointDataNotABoolError('Data is of type "{bad_type} and not of type "{good_type}"'.format(
                    bad_type = type(self.data),
                    good_type = bool
                ))

        # Return the create response dictionary
        return response_dict
#---------------------------------------------------------------------------------------------------
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
    TYPE_ERROR = 4      # For APIs that respond in error

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
        self.data_text = None

        # Paginating. If the 'paginate' option is set to True, the decorator will do the paginating.
        # A endpoint can choose to do this self by setting this option to False. This can be usefull
        # for endpoints that handle a lot of data.
        self.paginate = True
        self.page = None
        self.items_per_page = None
        self.last_page = None
        self.item_count = None
        self.all_item_count = None

        # For error objects, we have different variables
        self.error_code = None
        self.error_path = None
        self.error_text = 'Undefined error'
        self.error_traceback = None
        self.error_exception = None
        self.error_description = None
        self.error_show = False
    
    @property
    def response(self):
        """ Property to return the object itself as a dict """

        # Check if a valid type is set
        if not self.response_type in (APIResponse.TYPE_DATASET, APIResponse.TYPE_RECORD, APIResponse.TYPE_DONE, APIResponse.TYPE_ERROR):
            raise MeRESTAPIv1EndpointWrongResponseTypeError('Response type {response_type} is not valid'.format(
                response_type = self.response_type
            ))
        
        # If this is an error, we can create a simple dict and return it
        if self.response_type == APIResponse.TYPE_ERROR:
            # Define error texts
            error_texts = {
                '403': 'Not authorized for this resource',
                '404': 'Resource not found',
                '500': 'Server error'
            }

            # Find the correct error text
            if str(self.error_code) in error_texts:
                self.error_text = error_texts[str(self.error_code)]
            
            # Create a error-dict
            error_object = {
                'error': {
                    'code': self.error_code,
                    'text': self.error_text,
                    'path': self.error_path
                }
            }
            
            if self.error_show:
                # If we need to show exceptions, we add some values
                error_object['error']['traceback'] = self.error_traceback
                error_object['error']['exception'] = self.error_exception
                error_object['error']['description'] = self.error_description
            
            # Return the object
            return error_object
        
        # Calculate the runtime
        runtime = 0
        if self.starttime:
            runtime = round(time() - self.starttime, 3)

        # Create the default response dictionary
        response_dict = {
            'request': {
                'group': self.api_group,
                'endpoint': self.api_endpoint
            },
            'response': {
                'type': self.response_type,
                'runtime': runtime
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

                if self.last_page == 0:
                    self.last_page = 1

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
                'data_text': self.data_text,
                'page': self.page,
                'items_per_page': self.items_per_page,
                'last_page': self.last_page,
                'item_count': len(self.data),
                'all_item_count': self.all_item_count
            }
        
        # If this is single record, we have to add the data
        if self.response_type == self.TYPE_RECORD:
            # If we only have one record to return, we set it in the data
            response_dict['object'] = self.data
            response_dict['data_text'] = self.data_text
        
        # If this is done-thingy, we check if data is a boolean and if it is, we set that as the
        # return type
        if self.response_type == self.TYPE_DONE:
            if type(self.data) is bool:
                response_dict['success'] = self.data
                response_dict['data_text'] = self.data_text
            else:
                raise MeRESTAPIv1EndpointDataNotABoolError('Data is of type "{bad_type} and not of type "{good_type}"'.format(
                    bad_type = type(self.data),
                    good_type = bool
                ))

        # Return the create response dictionary
        return response_dict
#---------------------------------------------------------------------------------------------------
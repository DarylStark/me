#!/usr/bin/env python3
"""
    me_rest_api_v1 - api_users.py

    API module for '/users'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me_rest_api_v1 import MeRESTAPIv1
#---------------------------------------------------------------------------------------------------
@MeRESTAPIv1.register_group(name = 'users', description = 'User management')
class APIUsers:
    """ API class for 'users'. Can be used to list, edit and remove users """

    @MeRESTAPIv1.register_endpoint(group = 'users', name = 'user', description = 'Endpoint to retrieve, update or delete users')
    def user(*args, **kwargs):
        return 'User objects'
#---------------------------------------------------------------------------------------------------
#!/usr/bin/env python3
"""
    me_rest_api_v1 - api_oatuh.py

    API module for '/oatuh'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me_rest_api_v1 import MeRESTAPIv1
#---------------------------------------------------------------------------------------------------
@MeRESTAPIv1.register_group(name = 'oauth', description = 'OAuth authentication')
class APIOAuth:
    """ API class for 'oauth'. Can be used to authenticate """

    @MeRESTAPIv1.register_endpoint(
        group = 'oauth',
        name = 'validate',
        description = 'Validate API key',
        permissions = {
            'GET': 'oauth.validate'
        }
    )
    def validate(*args, **kwargs):
        return 'API validator'
#---------------------------------------------------------------------------------------------------
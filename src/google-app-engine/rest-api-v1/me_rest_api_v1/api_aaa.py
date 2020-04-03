#!/usr/bin/env python3
"""
    me_rest_api_v1 - api_aaa.py

    API module for '/aaa'
"""
#---------------------------------------------------------------------------------------------------
# Imports
from flask import request
from me_rest_api_v1 import MeRESTAPIv1
from me_rest_api_v1 import APIResponse
from me_rest_api_v1.exceptions import *
from database import DatabaseSession
from database import User
from database import APIUserToken
from database import APIClientToken
from database import APIUserPermission
import datetime
#---------------------------------------------------------------------------------------------------
@MeRESTAPIv1.register_group(name = 'aaa', description = 'Authentication and authorization')
class APIAAA:
    """ API class for 'aaa'. Can be used to authenticate and authorize """

    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'retrieve_user_token_with_credentials',
        description = 'Retrieve a user token with credentials',
        permissions = {
            'POST': 'aaa.retrieve_user_token_with_credentials'
        },
        user_token_needed = False
    )
    def retrieve_user_token_with_credentials(*args, **kwargs):
        """ Endpoint for clients to retrieve a user token using the users credentials. This can be
            used by clients who want to provide the user with a username and password instead of
            requesting them for a User Token.
            
            A retrieved user token will have a limited lifetime. After that, the token will expire
            and is not usable anymore. The amount of time for this is hardcoded into the application
            and cannot be changed. It is possible, however, to refresh the token with the
            'refresh_user_token' API endpoint.
        """
        
        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_RECORD)

        # Get the given username and password
        json_data = request.json

        # If no data is given, we raise an error
        if json_data is None or not type(json_data) is dict:
            raise MeRESTAPIv1AAARetrieveUserTokenNoDataError('No JSON data is given')

        # Check if we got a 'username' and a 'password'
        if not 'username' in json_data or not 'password' in json_data:
            raise MeRESTAPIv1AAARetrieveUserTokenNoDataError('No credentials given')

        # We checked evertyhing that needed to be checked. Let's start with the real endpoint. First
        # we check if the user exists
        with DatabaseSession(commit_on_end = True, expire_on_commit = False) as session:
            users = session.query(User).filter(User.username == json_data['username'])

            # If we don't have one user exactly, we cannot authorize
            if users.count() != 1:
                raise MeRESTAPIv1AAARetrieveUserTokenUserNotFoundError(f'User with username "{json_data["username"]}" is not found')

            # Get the user object
            user = users.first()

            # Check if a secret is filled in. If it is, we require two-factor authentication.
            if user.secret:
                # TODO: Implement this
                pass

            # Check if the given password is correct
            if not user.verify_password(json_data['password']):
                raise MeRESTAPIv1AAARetrieveUserTokenPasswordWrongError(f'The password for user "{json_data["password"]}" is not correct')

            # Find the client_key
            client_token = kwargs['client_token']
            client_token_object = session.query(APIClientToken).filter(APIClientToken.token == client_token).first()

            # Get how many hours a user-token will be valid before expiring. If this is set to '-1',
            # the session will never expire
            expirationdate = None
            expire_hours = MeRESTAPIv1.get_configuration('api', 'retrieved_user_key_lifetime')
            if expire_hours > 0:
                expirationdate = datetime.datetime.utcnow() + datetime.timedelta(hours = expire_hours)

            # Everything is correct! Let's create a UserToken object
            new_user_token = APIUserToken()
            new_user_token.user = user.id
            new_user_token.expiration = expirationdate
            new_user_token.client_token = client_token_object.id
            new_user_token.enabled = True
            new_user_token.generate_random_token()

            # Add the token
            session.add(new_user_token)

            # Set the token in the response
            response.data = new_user_token

            # Do a intermediate commit so the user token gets added and a 'id' is given
            session.commit()

            # Copy all permissions from the client token to the user token
            for permission in client_token_object.client_permissions:
                user_permission = APIUserPermission()
                user_permission.permission = permission.permission
                user_permission.user_token = new_user_token.id
                user_permission.granted = permission.granted
                session.add(user_permission)

        # Return the response
        return response
    
    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'refresh_user_token',
        description = 'Refersh a user token',
        permissions = {
            'POST': 'aaa.refresh_user_token'
        },
        user_token_needed = True
    )
    def refresh_user_token(*args, **kwargs):
        return None
#---------------------------------------------------------------------------------------------------
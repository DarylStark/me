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
from database import APIPermission
from database import APIClientToken
from database import APIUserPermission
import datetime
import pyotp
from sqlalchemy import and_
import re
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

            The body of the request should be a JSON object with the following keys:
            - 'username': the username of the user
            - 'password': the password of the user
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

            # Check if a secret is filled in. If it is, we require two-factor authentication. To
            # signal this to the client, we return a response with '2nd-factor-required'. The client
            # can then ask the user for the 2nd factor.
            if user.second_factor_enabled and not '2nd_factor' in json_data.keys():
                response.data = {
                    '_type': '2nd_factor',
                    '2nd_factor_required': True
                }
                return response

            # Check if the given password is correct
            if not user.verify_password(json_data['password']):
                raise MeRESTAPIv1AAARetrieveUserTokenPasswordWrongError(f'The password for user "{json_data["username"]}" is not correct')

            # Find the client token
            client_token = kwargs['client_token']
            client_token_object = session.query(APIClientToken).filter(APIClientToken.token == client_token).first()

            # Get how many hours a user-token will be valid before expiring. If this is set to '-1',
            # the session will never expire
            expirationdate = None
            expire_hours = MeRESTAPIv1.get_configuration('api', 'retrieved_user_key_lifetime')
            if expire_hours > 0:
                expirationdate = datetime.datetime.utcnow() + datetime.timedelta(hours = expire_hours)
            
            # If a 2nd factor was required and the key is given, we can check if it is correct
            if user.second_factor_enabled and '2nd_factor' in json_data.keys():
                factor = json_data['2nd_factor']
                if factor != pyotp.TOTP(user.secret).now():
                    # Second factor was wrong. Give an error for the user
                    raise MeRESTAPIv1AAARetrieveUserTokenFactorWrongError(f'The 2nd factor for user "{json_data["username"]}" is not correct')

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
        description = 'Refresh a user token',
        permissions = {
            'PATCH': 'aaa.refresh_user_token'
        },
        user_token_needed = True
    )
    def refresh_user_token(*args, **kwargs):
        """ Endpoint for users to refresh their user token. This can be used by (web-) clients to
            refresh the user token before it expires. If the token has no expiration date, this API
            call fails. The token will be refreshed by the amound of hours that is set in the value
            for 'retrieved_user_key_refresh_lifetime' in the API configuration. If the current
            lifetime of the token is greater then the value of this configuration, this API call will
            fail.

            The request doesn't need a body. The API will use the provided User Token to update it.
        """

        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_RECORD)

        # Get the value for the configuration-item
        expire_hours = MeRESTAPIv1.get_configuration('api', 'retrieved_user_key_refresh_lifetime')

        # Get the APIUserToken-object and update the expire time
        with DatabaseSession(commit_on_end = True, expire_on_commit = False) as session:
            # Get the APIUserToken
            user_token_object = session.query(APIUserToken).filter(APIUserToken.token == kwargs['user_token']).first()

            # Check if the current expiration is far away enough
            if user_token_object.expiration is None:
                raise MeRESTAPIv1AARefreshUserTokenInfiniteTokenError('The expirationdate for this token is set to "not expire" and cannot be refreshed')

            # Check how long this token is still valid
            now = datetime.datetime.utcnow()
            difference = user_token_object.expiration - now
            difference_hours = difference.total_seconds() / 3600

            # Check if the difference in hours is greater then the configured time to refresh the
            # token. If it is, we raise an error cause that is not permitted.
            if difference_hours > expire_hours:
                raise MeRESTAPIv1AARefreshUserTokenNotExpiringYetTokenError(f'The expirationdate for this token is still {difference_hours} valid and therefor not a candidate to be refreshed')

            # Calculate the new expirationdate
            expirationdate = datetime.datetime.utcnow() + datetime.timedelta(hours = expire_hours)
            user_token_object.expiration = expirationdate

            # Set the token in the response
            response.data = user_token_object

        return response
    
    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'remove_user_token',
        description = 'Remove a user token',
        permissions = {
            'DELETE': 'aaa.remove_user_token'
        },
        user_token_needed = True
    )
    def remove_user_token(*args, **kwargs):
        """ Endpoint for users to reomove their user token. Can be used by clients to 'logoff' a
            user.

            The request doesn't need a body. The API will use the provided User Token to update it.
        """

        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_DONE)
        response.data = False

        # Get the APIUserToken-object and update the expire time
        with DatabaseSession(commit_on_end = True) as session:
            # Get the UserToken
            user_token_object = session.query(APIUserToken).filter(APIUserToken.token == kwargs['user_token']).first()

            # Delete all permission connected to this UserToken
            for permission in user_token_object.user_permissions:
                session.delete(permission)
            
            # Delete the UserToken
            session.delete(user_token_object)
        
        # Set the response to True and return it
        response.data = True
        return response

    
    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'user_permissions',
        description = 'Retrieve and update a users permissions',
        permissions = {
            'GET': 'aaa.retrieve_user_permissions',
            'PATCH': 'aaa.update_user_permissions'
        },
        user_token_needed = True
    )
    def user_permissions(*args, **kwargs):
        """ Endpoint for users to retrieve and update its permissions. This endpoint will list all
            permissions that are enabled for this user, or set permissions to granted or not granted
        """

        # Get the token that the user wants to see the permissions from or edit from
        user_token = None
        if request.method == 'GET':
            if not request.args.get('user_token') is None:
                user_token = request.args.get('user_token')
        elif request.method == 'PATCH':
            json_data = request.json
            if 'user_token' in json_data.keys():
                user_token = json_data['user_token']
        
        if user_token is None:
            user_token = kwargs['user_token']

        # We got the correct token, let's execute the API endpoint
        if request.method == 'GET':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_DATASET)
            
            # Get all permissions from the database
            with DatabaseSession() as session:
                # Find the current user
                user_token_object = session.query(APIUserToken).filter(APIUserToken.token == kwargs['user_token']).first()

                # Get the token object
                user_token_object = session.query(APIUserToken).filter(and_(APIUserToken.token == user_token, APIUserToken.user == user_token_object.user)).first()

                # If we didn't get a token, either because it doesn't exists or is not for the
                # current user, we raise an error
                if user_token_object is None:
                    raise MeRESTAPIv1AAAUserPermissionsTokenNotFoundError(f'Usertoken "{user_token}" can not be found')

                # Get the permissions objects from the user token object
                token_permission_objects = [ { 'permission': permission.permission_object, 'granted': permission.granted } for permission in user_token_object.user_permissions ]

                # Get all IDs in the token_permission_objects
                token_permission_objects_ids = [ permission['permission'].id for permission in token_permission_objects ]

                # Get all available permissions
                permission_objects = session.query(APIPermission).all()

                # Get the missing permissions
                missing_permissions = [ { 'permission': permission, 'granted': False } for permission in permission_objects if not permission.id in token_permission_objects_ids ]

                # Create a list with all the permissions combined
                return_list = list()
                
                # Add the permission objects from the token
                combined = token_permission_objects + missing_permissions
                for permission in  combined:
                    return_list.append({
                        'id': permission['permission'].id,
                        'description': permission['permission'].description,
                        'section': permission['permission'].section,
                        'subject': permission['permission'].subject,
                        'granted': permission['granted'],
                    })
            
            # Set the sorted return data
            return_list.sort(key = lambda x: x['section'] + '.' + x['subject'])
            response.data = return_list

            # Return the object
            return response
        
        if request.method == 'PATCH':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_DONE)

            # Verify that we have all the needed options in the request data
            if not 'permission' in json_data.keys() or not 'granted' in json_data.keys():
                raise MeRESTAPIv1AAAUserPermissionsNotAllFieldsError('Not all fields are specified. Fields "permission" and "granted" should be given')
            
            if not type(json_data['permission']) is str or not type(json_data['granted']) is bool:
                raise MeRESTAPIv1AAAUserPermissionsNotAllFieldsError('Field "permission" should be a string and "granted" a boolean')

            if not re.match('[a-z0-9_]+\.[a-z0-9_]+', json_data['permission']):
                raise MeRESTAPIv1AAAUserPermissionsNotAllFieldsError('Field "permission" should be a in form "<section>.<subject>')
            
            # Get all permissions from the database
            with DatabaseSession(commit_on_end = True) as session:
                # Find the current user
                user_token_object = session.query(APIUserToken).filter(APIUserToken.token == kwargs['user_token']).first()

                # Get the token object
                user_token_object = session.query(APIUserToken).filter(and_(APIUserToken.token == user_token, APIUserToken.user == user_token_object.user)).first()

                # If we didn't get a token, either because it doesn't exists or is not for the
                # current user, we raise an error
                if user_token_object is None:
                    raise MeRESTAPIv1AAAUserPermissionsTokenNotFoundError(f'Usertoken "{user_token}" can not be found')
                
                # Find the permissions
                section, subject = re.findall('^([a-z0-9_]+)\.([a-z0-9_]+)$', json_data['permission'])[0]
                permission_objects = session.query(APIPermission).filter(and_(
                    APIPermission.section == section,
                    APIPermission.subject == subject
                ))

                # Give an error if we don't have one permissions
                if permission_objects.count() != 1:
                    raise MeRESTAPIv1AAAUserPermissionsPermissionNotFoundError(f'Permission "{section}.{subject}" can not be found')
                
                # Get the object
                permission_object = permission_objects.first()

                # Find the APIUserPermission object
                api_user_permission_object = session.query(APIUserPermission).filter(and_(
                    APIUserPermission.user_token == user_token_object.id,
                    APIUserPermission.permission == permission_object.id
                )).first()

                # Check if we have any
                if not api_user_permission_object is None:
                    api_user_permission_object.granted = json_data['granted']
                else:
                    # Permission didn't exist. Let's create it
                    api_user_permission_object = APIUserPermission(
                        user_token = user_token_object.id,
                        permission = permission_object.id,
                        granted = json_data['granted']
                    )
                    session.add(api_user_permission_object)
                
            # Set the response data
            response.data = True

            # Return the object
            return response
    
    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'verify_user_token',
        description = 'Verify a user token',
        permissions = {
            'GET': 'aaa.verify_user_token'
        },
        user_token_needed = True
    )
    def verify_user_token(*args, **kwargs):
        """ Endpoint for users to verify if they are using a valid User Token. this endpoints
            respons with a UserToken object for the user """
        
        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_RECORD)
        
        # Get all permissions from the database
        with DatabaseSession() as session:
            # Find the user token
            user_token = kwargs['user_token']
            user_token_object = session.query(APIUserToken).filter(APIUserToken.token == user_token).first()
            
            response.data = user_token_object

        # Return the object
        return response
    
    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'user_object',
        description = 'Manage the own user object',
        permissions = {
            'GET': 'aaa.get_user_object',
            'PATCH': 'aaa.update_user_object'
        },
        user_token_needed = True
    )
    def user_object(*args, **kwargs):
        """ Endpoint for users to retrieve and update their user object """
        
        # GET: retrieve the user object
        if request.method.upper() == 'GET':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_RECORD)
            
            # Get the user object from the database
            with DatabaseSession() as session:
                # Find the user token
                user_token = kwargs['user_token']
                user_token_object = session.query(APIUserToken).filter(APIUserToken.token == user_token).first()
                
                response.data = user_token_object.user_object

            # Return the object
            return response
        
        # PATCH: update the user object
        if request.method.upper() == 'PATCH':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_DONE)
            response.data = True

            # Get the data
            json_data = request.json

            # Get the user object from the database
            with DatabaseSession(commit_on_end = True) as session:
                # Find the user token
                user_token = kwargs['user_token']
                user_token_object = session.query(APIUserToken).filter(APIUserToken.token == user_token).first()

                # Change the given fields after verifing them
                if 'username' in json_data.keys():
                    if len(json_data['username']) > 3:
                        # Check if this username is unique
                        user_username_count = session.query(User).filter(and_(User.username == json_data['username'], User.id != user_token_object.user_object.id)).count()
                        if user_username_count == 0:
                            user_token_object.user_object.username = json_data['username']
                        else:
                            response.data = False
                            response.data_text = 'username_in_use'
                            return response
                    else:
                        response.data = False
                        response.data_text = 'username_invalid'
                        return response

                if 'fullname' in json_data.keys():
                    if len(json_data['fullname']) > 3:
                        user_token_object.user_object.fullname = json_data['fullname']
                    else:
                        response.data = False
                        response.data_text = 'fullname_invalid'
                        return response
                
                if 'email' in json_data.keys():
                    if re.match('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', json_data['email']):
                        # Check if this emailaddress is unique
                        user_email_count = session.query(User).filter(and_(User.email == json_data['email'], User.id != user_token_object.user_object.id)).count()
                        if user_email_count == 0:
                            user_token_object.user_object.email = json_data['email']
                        else:
                            response.data = False
                            response.data_text = 'email_in_use'
                            return response
                    else:
                        response.data = False
                        response.data_text = 'email_invalid'
                        return response

            # Return the object
            return response

    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'change_password',
        description = 'Change the password for the current user',
        permissions = {
            'PATCH': 'aaa.change_password'
        },
        user_token_needed = True
    )
    def change_password(*args, **kwargs):
        """ Endpoint for users to change their password """

        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_DONE)
        response.data = True

        # Get the data
        json_data = request.json

        if not 'current_pw' in json_data.keys() or not 'new_pw' in json_data.keys():
            raise MeRESTAPIv1AAAChangePasswordMissingFieldsError('Not all fields are specified. Need "current_pw" and "new_pw"')
        
        # Verify the lenght of the new password
        if len(json_data['new_pw']) < 8:
            response.data = False
            response.data_text = 'new_pw_too_short'
            return response

        # Get the user object from the database
        with DatabaseSession(commit_on_end = True) as session:
            # Get the user object
            user_token = kwargs['user_token']
            user = session.query(APIUserToken).filter(APIUserToken.token == user_token).first().user_object

            # Verify the 'current pw'
            if not user.verify_password(json_data['current_pw']):
                response.data = False
                response.data_text = 'current_pw'
                return response
            
            # Check if the new password is different from the current password
            if json_data['new_pw'] == json_data['current_pw']:
                response.data = False
                response.data_text = 'new_pw_equal_to_current'
                return response
            
            # Update the password
            user.set_password(json_data['new_pw'])

        # Return the response
        return response
    
    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'disable_two_factor',
        description = 'Disable two-factor authentication for the current user',
        permissions = {
            'PATCH': 'aaa.disable_two_factor'
        },
        user_token_needed = True
    )
    def disable_two_factor(*args, **kwargs):
        """ Endpoint for users to disable two-factor authentication """

        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_DONE)
        response.data = True

        # Get the user object from the database
        with DatabaseSession(commit_on_end = True) as session:
            # Get the user object
            user_token = kwargs['user_token']
            user = session.query(APIUserToken).filter(APIUserToken.token == user_token).first().user_object
            user.secret = None
            user.secret_verified = False
        
        # Return the response
        return response
    
    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'enable_two_factor',
        description = 'Enable two-factor authentication for the current user',
        permissions = {
            'PATCH': 'aaa.enable_two_factor'
        },
        user_token_needed = True
    )
    def enable_two_factor(*args, **kwargs):
        """ Endpoint for users to enable two-factor authentication """

        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_RECORD)

        # Get the user object from the database
        with DatabaseSession(commit_on_end = True) as session:
            # Get the user object
            user_token = kwargs['user_token']
            user = session.query(APIUserToken).filter(APIUserToken.token == user_token).first().user_object

            # Check if second factor is already enabled
            if user.second_factor_enabled:
                raise MeRESTAPIv1AAAEnableTwoFactorAlreadyEnabledError('Second factor authentication is already enabled for this user')

            # Generate a new secret key and return it to the user
            user.generate_secret()
            response.data = { 'type': '_secret', 'secret': user.secret }
        
        # Return the response
        return response
    
    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'verify_two_factor',
        description = 'Verify two-factor authentication for the current user',
        permissions = {
            'PATCH': 'aaa.verify_two_factor'
        },
        user_token_needed = True
    )
    def verify_two_factor(*args, **kwargs):
        """ Endpoint for users to verify their two-factor authentication """

        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_DONE)
        response.data = True

        # Get the data
        json_data = request.json

        # Check if the '2nd_factor' is in the request
        if not '2nd_factor' in json_data.keys():
            raise MeRESTAPIv1AAAVerifyTwoFactorMissingFieldsError('Not all fields are specified. Need "2nd_factor"')

        # Get the user object from the database
        with DatabaseSession(commit_on_end = True) as session:
            # Get the user object
            user_token = kwargs['user_token']
            user = session.query(APIUserToken).filter(APIUserToken.token == user_token).first().user_object

            # Check if second factor is disabled for the user
            if user.second_factor_enabled == True:
                raise MeRESTAPIv1AAAVerifyTwoFactorAlreadyEnabledError('Second factor authentication is already enabled for this user')

            # Check if the given value is correct
            factor = json_data['2nd_factor']
            factor_should_be = pyotp.TOTP(user.secret).now()
            if factor == factor_should_be:
                user.secret_verified = True
            else:
                user.secret_verified = False
                response.data = False
                response.data_text = '2nd_factor'
        
        # Return the response
        return response
    
    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'user_token',
        description = 'Create, retrieve, update or delete API Client tokens',
        permissions = {
            'POST': 'aaa.create_user_token',
            'GET': 'aaa.retrieve_user_token',
            'PATCH': 'aaa.update_user_token',
            'DELETE': 'aaa.delete_user_token'
        },
        user_token_needed = True
    )
    def user_token(*args, **kwargs):
        """ Endpoint for users to create, retrieve, update or delete API user tokens """

        if request.method.upper() == 'POST':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_RECORD)

            # Get the given data
            json_data = request.json

            # Check if we got an 'client-id'
            if not 'client_id' in json_data.keys():
                raise MeRESTAPIv1AAACreateUserTokenMissingClientIDError('Missing "client_id" in data')
            
            # Start a database session
            with DatabaseSession(commit_on_end = True, expire_on_commit = False) as session:
                # Check if the given client-token exists
                client_tokens = session.query(APIClientToken).filter(APIClientToken.id == json_data['client_id'])
                if client_tokens.count() != 1:
                    raise MeRESTAPIv1AAACreateUserTokenClientNotFoundError(f'Client with id {json_data["client_id"]} is not found')
                
                # Get the APIUserToken
                user_token_object = session.query(APIUserToken).filter(APIUserToken.token == kwargs['user_token']).first()

                # Create a new UserToken
                new_user_token = APIUserToken(
                    user = user_token_object.user,
                    client_token = json_data['client_id']
                )

                # Generate a random token
                new_user_token.generate_random_token()

                # Add the token
                session.add(new_user_token)

                # Set the token in the response
                response.data = new_user_token

                # Do a intermediate commit so the user token gets added and a 'id' is given
                session.commit()

                # Copy all permissions from the client token to the user token
                for permission in client_tokens.first().client_permissions:
                    user_permission = APIUserPermission()
                    user_permission.permission = permission.permission
                    user_permission.user_token = new_user_token.id
                    user_permission.granted = permission.granted
                    session.add(user_permission)
            
            # Return the response
            return response

        if request.method.upper() == 'GET':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_DATASET)
            
            # Get all user tokens from the database
            with DatabaseSession() as session:
                # Get the users token that the user is using now so we can retrieve the user that
                # belongs to it
                user_token_object = session.query(APIUserToken).filter(APIUserToken.token == kwargs['user_token']).first()
                user_tokens = session.query(APIUserToken).filter(APIUserToken.user == user_token_object.user)
            
            # Set the return data
            response.data = user_tokens.all()

            # Return the object
            return response
        
        if request.method.upper() == 'PATCH':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_DONE)

            # Get the given data
            json_data = request.json

            # Check if we got an 'id'
            if not 'id' in json_data.keys():
                raise MeRESTAPIv1AAAUpdateUserTokenMissingIDError('Missing "id" in data')

            # Start a database session
            with DatabaseSession(commit_on_end = True) as session:
                # Get the users token that the user is using now so we can retrieve the user that
                # belongs to it
                user_token_object = session.query(APIUserToken).filter(APIUserToken.token == kwargs['user_token']).first()

                # Find the given token
                user_tokens = session.query(APIUserToken).filter(and_(APIUserToken.id == json_data['id'], APIUserToken.user == user_token_object.user))

                # Check if we got a user token
                if user_tokens.count() != 1:
                    raise MeRESTAPIv1AAAUpdateUserTokenMissingNotFoundError(f'Usertoken with id {json_data["id"]} can not be found')

                # Get the token to update
                token_object = user_tokens.first()

                # Update the 'expire' field
                if 'expire' in json_data.keys():
                    try:
                        # Verify the expire
                        if json_data['expire'] is None:
                            token_object.expiration = None
                        else:
                            expire_datetime = datetime.datetime.fromisoformat(json_data['expire'])
                            token_object.expiration = expire_datetime
                    except ValueError:
                        raise MeRESTAPIv1AAAUpdateUserTokenWrongFieldFormatError(f'The date "{json_data["expire"]}" is not in the correct format')
                
                # Update the 'description' field
                if 'description' in json_data.keys():
                    token_object.description = json_data['description']
                    if json_data['description'].strip() == '':
                        token_object.description = None
                
                # Update the 'enabled' field
                if 'enabled' in json_data.keys():
                    token_object.enabled = json_data['enabled']

                # Set the response to True so the caller knows everything went OK
                response.data = True
            
            return response

        if request.method.upper() == 'DELETE':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_DONE)

            # Get the given data
            json_data = request.json

            # Check if we got an 'id'
            if not 'id' in json_data.keys():
                raise MeRESTAPIv1AAADeleteUserTokenMissingIDError('Missing "id" in data')
            
            # Start a database session
            with DatabaseSession(commit_on_end = True) as session:
                # Get the users token that the user is using now so we can retrieve the user that
                # belongs to it
                user_token_object = session.query(APIUserToken).filter(APIUserToken.token == kwargs['user_token']).first()

                # Find the given token
                user_tokens = session.query(APIUserToken).filter(and_(APIUserToken.id == json_data['id'], APIUserToken.user == user_token_object.user))

                # Check if we got a user token
                if user_tokens.count() != 1:
                    raise MeRESTAPIv1AAADeleteUserTokenMissingNotFoundError(f'User-tken with id {json_data["id"]} can not be found')

                # Get the token to update
                token_object = user_tokens.first()

                # Delete all permission connected to this UserToken
                for permission in token_object.user_permissions:
                    session.delete(permission)

                # Delete the token
                session.delete(token_object)
            
            # Return the response
            response.data = True
            return response
    
    @MeRESTAPIv1.register_endpoint(
        group = 'aaa',
        name = 'set_token_description',
        description = 'Set a session description for the current session for the current user',
        permissions = {
            'PATCH': 'aaa.set_token_description'
        },
        user_token_needed = True
    )
    def set_token_description(*args, **kwargs):
        """ Endpoint for users to set a description to their current token """

        # Create an empty response object
        response = APIResponse(APIResponse.TYPE_DONE)

        # Get the given data
        json_data = request.json

        # Check if we got an 'description'
        if not 'description' in json_data.keys():
            raise MeRESTAPIv1AAASetTokenDescriptionMissingDescriptionError('Missing "description" in data')

        # Get the user object from the database
        with DatabaseSession(commit_on_end = True) as session:
            # Get the user object
            user_token_object = session.query(APIUserToken).filter(APIUserToken.token == kwargs['user_token']).first()

            # Generate a new secret key and return it to the user
            user_token_object.description = json_data['description']
            if json_data['description'].strip() == '':
                user_token_object.description = None

            response.data = True
        
        # Return the response
        return response
#---------------------------------------------------------------------------------------------------

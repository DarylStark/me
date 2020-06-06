#!/usr/bin/env python3
"""
    me_rest_api_v1 - api_api_clients.py

    API module for '/api_clients'
"""
#---------------------------------------------------------------------------------------------------
# Imports
import re
from flask import request
from me_rest_api_v1 import MeRESTAPIv1
from me_rest_api_v1 import APIResponse
from me_rest_api_v1.exceptions import *
from database import DatabaseSession
from database import APIClientToken
from database import APIClientPermission
from database import APIPermission
from sqlalchemy import and_
#---------------------------------------------------------------------------------------------------
@MeRESTAPIv1.register_group(name = 'api_clients', description = 'API Client management')
class APIAPIClients:
    """ API class for 'api_clients'. Can be used to manage API clients """

    @MeRESTAPIv1.register_endpoint(
        group = 'api_clients',
        name = 'client',
        description = 'Create, retrieve, update or delete API Client tokens',
        permissions = {
            'POST': 'api_clients.create_client_token',
            'GET': 'api_clients.retrieve_client_token',
            'PATCH': 'api_clients.update_client_token'
        },
        user_token_needed = True
    )
    def client(*args, **kwargs):
        """ Endpoint for users to create, retrieve, update or delete API client tokens """

        if request.method.upper() == 'POST':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_RECORD)

            # Get the given data
            json_data = request.json

            # Check if we got the correct fields in the reqest
            if not 'name' in json_data.keys() or not 'version' in json_data.keys() or not 'publisher' in json_data.keys():
                raise MeRESTAPIv1APIClientsCreateClientTokenMissingFieldsError(f'Not all fields are specified; missing "name", "version" or "publisher"')

            # Start a database session
            with DatabaseSession(commit_on_end = True, expire_on_commit = False) as session:
                # Create a new APIClientToken
                new_client_token = APIClientToken(
                    expiration = None,
                    app_name = json_data['name'],
                    app_version = json_data['version'],
                    app_publisher = json_data['publisher'],
                )

                # Generate a random token
                new_client_token.generate_random_token()

                # Add the token
                session.add(new_client_token)

                # Set the token in the response
                response.data = new_client_token

            # Return the response
            return response

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
    
    @MeRESTAPIv1.register_endpoint(
        group = 'api_clients',
        name = 'permissions',
        description = 'Retrieve the permissions for a specific API client',
        permissions = {
            'GET': 'api_clients.retrieve_client_permissions',
            'PATCH': 'api_clients.update_client_permissions'
        },
        user_token_needed = True
    )
    def permissions(*args, **kwargs):
        """ Endpoint to retrieve permissions for a specific API client """

        # Get the token that the user wants to see the permissions from or edit from
        client_token = None
        if request.method == 'GET':
            if not request.args.get('token') is None:
                client_token = request.args.get('token')
        elif request.method == 'PATCH':
            json_data = request.json
            if 'token' in json_data.keys():
                client_token = json_data['token']
        
        if client_token is None:
            client_token = kwargs['client_token']

        # We got the correct token, let's execute the API endpoint
        if request.method == 'GET':
            # Create an empty response object
            response = APIResponse(APIResponse.TYPE_DATASET)
            
            # Get all permissions from the database
            with DatabaseSession() as session:
                # Get the token object
                client_token_object = session.query(APIClientToken).filter(APIClientToken.token == client_token).first()

                # If we didn't get a token we raise an error
                if client_token_object is None:
                    raise MeRESTAPIv1APIClientsPermissionsTokenNotFoundError(f'Client token "{client_token}" can not be found')

                # Get the permissions objects from the client token object
                token_permission_objects = [ { 'permission': permission.permission_object, 'granted': permission.granted } for permission in client_token_object.client_permissions ]

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
                raise MeRESTAPIv1APIClientsPermissionsNotAllFieldsError('Not all fields are specified. Fields "permission" and "granted" should be given')
            
            if not type(json_data['permission']) is str or not type(json_data['granted']) is bool:
                raise MeRESTAPIv1APIClientsPermissionsNotAllFieldsError('Field "permission" should be a string and "granted" a boolean')

            if not re.match('[a-z0-9_]+\.[a-z0-9_]+', json_data['permission']):
                raise MeRESTAPIv1APIClientsPermissionsNotAllFieldsError('Field "permission" should be a in form "<section>.<subject>')
            
            # Get all permissions from the database
            with DatabaseSession(commit_on_end = True) as session:
                # Get the token object
                client_token_object = session.query(APIClientToken).filter(APIClientToken.token == client_token).first()

                # If we didn't get a token, either because it doesn't exists or is not for the
                # current user, we raise an error
                if client_token_object is None:
                    raise MeRESTAPIv1APIClientsPermissionsTokenNotFoundError(f'Client token "{client_token}" can not be found')
                
                # Find the permissions
                section, subject = re.findall('^([a-z0-9_]+)\.([a-z0-9_]+)$', json_data['permission'])[0]
                permission_objects = session.query(APIPermission).filter(and_(
                    APIPermission.section == section,
                    APIPermission.subject == subject
                ))

                # Give an error if we don't have one permissions
                if permission_objects.count() != 1:
                    raise MeRESTAPIv1APIClientsPermissionsPermissionNotFoundError(f'Permission "{section}.{subject}" can not be found')
                
                # Get the object
                permission_object = permission_objects.first()

                # Find the APIClientPermission object
                api_client_permission_object = session.query(APIClientPermission).filter(and_(
                    APIClientPermission.client_token == client_token_object.id,
                    APIClientPermission.permission == permission_object.id
                )).first()

                # Check if we have any
                if not api_client_permission_object is None:
                    api_client_permission_object.granted = json_data['granted']
                else:
                    # Permission didn't exist. Let's create it
                    api_client_permission_object = APIClientPermission(
                        client_token = client_token_object.id,
                        permission = permission_object.id,
                        granted = json_data['granted']
                    )
                    session.add(api_client_permission_object)
                
            # Set the response data
            response.data = True

            # Return the object
            return response
#---------------------------------------------------------------------------------------------------
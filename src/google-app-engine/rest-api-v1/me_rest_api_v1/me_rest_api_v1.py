#!/usr/bin/env python3
"""
    me_rest_api_v1 - me_rest_api_v1.py

    Contains the main class for the Rest API v1 part of the  application. This class, called
    MeRESTAPIv1, can be used to run the version 1 of the API for the Me application.

    The class is meant to be run as a static class; it is impossible to create instances of it.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me_rest_api_v1.exceptions import *
from me_rest_api_v1 import APIResponse
from me_rest_api_v1 import MeJSONEncoder
from database import Database
from database import DatabaseSession
from database import APIUserToken
from database import APIClientToken
from database import APIClientLogEntry
from database import APIUserLogEntry
from time import time
from sqlalchemy import and_
from flask import request
import flask
import json
import re
import datetime
import traceback
import logging
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1:
    """ Main class for the REST API. Should be used as a static class """

    # Class attributes for Flask;
    # - The 'flask_app' is a class attribute that will be used as the main object for Flask. All
    #   Flask requests will be using this.
    # - The 'registered_groups' will be a dictionary. The keys are going to be API group names
    #   that can match a specific URL to a specific class. Within this class, methods will be
    #   created for the specific API groups that are going to be used
    
    flask_app = flask.Flask(__name__)
    registered_groups = {}

    # Class attributes;
    # - The 'configfile' is the file contains all the configuration for the application. It defaults
    #   to 'me-configuration.json', but can be changed by the calling script
    # - The 'config' will be the dict that contains the actual config.
    # - The 'environment' tells the class what environment we are in. The environment has to match a
    #   JSON key configuration file
    # - The 'starttime' is the starttime of the application (in UTC). This is set so we can see when
    #   the instance was started. The user can retrieve this using the REST API.

    configfile = 'apiv1-configuration.json'
    config = None
    environment = None
    starttime = datetime.datetime.utcnow()

    # We create a logger for application-level logging. This logger is meant to log application
    # events, not accounting details for API clients.
    logger = logging.getLogger('MeRESTAPIv1')

    # Methods to make sure this class is used as it is suppoes to be
    def __new__(cls):
        """ When someone tries to create a instance of it, we give an error """
        raise TypeError('It is impossible to create a instance of class "{classname}"'.format(
            classname = cls.__name__
        ))

    @classmethod
    def load_config(cls):
        """ Load the configuration file """
        try:
            with open(cls.configfile, 'r') as cfgfile:
                cls.config = json.load(cfgfile)
        except FileNotFoundError:
            raise MeRESTAPIv1ConfigFileError('File "{file}" doesn\'t exist'.format(file = cls.configfile))
        except json.decoder.JSONDecodeError:
            raise MeRESTAPIv1ConfigFileError('File "{file}" is not a valid JSON file'.format(file = cls.configfile))

    @classmethod
    def set_environment(cls, environment):
        """ Set the environment of the configuration to use. Checks first if this environment is
            available in the configuration """
        
        # Check if the configuration is still None. If it is, load the configuration first
        if cls.config is None:
            cls.load_config()

        # Check if the asked environment exists and try to set it. If we get an AttributeError,
        # the configuration is still 'None'. We have to give the user a error in that specific
        # case.
        if environment in cls.config.keys():
            cls.environment = environment
        else:
            raise MeRESTAPIv1ConfigFileError('Configuration environment "{environment}" does not exist'.format(environment = environment))
    
    @classmethod
    def get_configuration(cls, group, setting = None):
        """ Returns a configuration setting for a given group (like 'database') and a given setting
            (like 'username'). If 'setting' is not given, the complete dict for the group is
            returned """
        
        # Check if a environment is set. If it isn't, we stop
        if cls.environment is None:
            raise MeRESTAPIv1ConfigFileError('Environment isn\'t set! Please set environment first')

        # Check if the configuration is set and load it if it isn't
        if cls.config is None:
            cls.load_config()
        
        # Check if the given group exists
        if group in cls.config[cls.environment].keys():
            # If a setting is given ...
            if setting:
                # ... check if the settings exists
                if setting in cls.config[cls.environment][group].keys():
                    # Return the setting
                    return cls.config[cls.environment][group][setting]
                else:
                    # If the setting doesn't exist, raise an error
                    raise MeRESTAPIv1ConfigFileError('Configuration group "{group}" does not contain a setting "{setting}"'.format(group = group, setting = setting))
            else:
                # If no setting is given, we return the complete dict for the group
                return cls.config[cls.environment][group]
        else:
            raise MeRESTAPIv1ConfigFileError('Configuration group "{group}" does not exist'.format(group = group))
    
    @classmethod
    def initiate(cls):
        """ Method to do everything that needs to be done before the application can be started.
            This method will create the database connection and will make sure all tables in this
            database get created """
        
        # Check if the configuration is still None. If it is, load the configuration first
        if cls.config is None:
            cls.load_config()
        
        # Configure the logger
        cls.logger.info('Logging started')
        
        # Get the database configuration
        sql_settings = cls.get_configuration(group = 'database')

        # There are a few ways to connect to the MySQL server. The first way is connecting the
        # normal way using a TCP socket. The other way is with a Unix socket. This last method is
        # used by Google App Engine. In the configuration file, it is possible to specify what
        # method to use
        if sql_settings['use_socket']:
            connection_string = 'mysql+pymysql://{username}:{password}@/{database}?unix_socket=/cloudsql/{sql_instance}'
        else:
            connection_string = 'mysql+pymysql://{username}:{password}@{server}/{database}'
        
        # Create a database connection. This will also add any tables that need to be added.
        cls.logger.info('Connecting to the database')
        Database.connect(
            connection_string.format(**sql_settings),
            **cls.get_configuration(group = 'sqlalchemy')
        )
        cls.logger.info('Connected to database')
    
    @staticmethod
    def get_error_response(error, error_code, path):
        """ Return a APIResponse-object for a error """

        # Create a error response object
        error_object = APIResponse(APIResponse.TYPE_ERROR)
        error_object.error_path = path
        error_object.error_code = error_code
        error_object.error_traceback = traceback.format_exception(etype = type(error), value = error, tb = error.__traceback__)
        error_object.error_exception = error.__class__.__name__
        error_object.error_description = str(error)
        error_object.error_show = MeRESTAPIv1.get_configuration('errors', 'show_exceptions')

        # Return the created error object
        json_options = dict()
        if 'pretty' in request.args.keys():
            json_options = {
                'indent': 4,
                'sort_keys': True
            }
        
        # If this error is something else then a 403 or 404 error, we have to log it
        if error_code >= 500:
            MeRESTAPIv1.logger.error(f'Error {error_code} during request for "{path}": "{error.__class__.__name__}"\n', exc_info = True)

        # Return the new Flask Response
        return flask.Response(json.dumps(error_object.response, cls = MeJSONEncoder, **json_options), mimetype = 'application/json', status = error_code)

    @classmethod
    def start(cls):
        """ The start method start the actual application """

        cls.logger.info('Starting application')

        # Start Flask with the configuration that is red in
        return cls.flask_app.run(**cls.get_configuration('flask'))
    
    @flask_app.route('/', defaults = { 'path': '' }, methods = ['GET', 'POST', 'PATCH', 'DELETE'])
    @flask_app.route('/<path:path>', methods = ['GET', 'POST', 'PATCH', 'DELETE'])
    def api_endpoint(path):
        """ Show the correct page based on registered classes expressions """
        
        # Because we use services in Google App Engine with a dispatch.yaml file, we still have the
        # route from the dispatcher in the URL. In the configuration file, this URL is set and we
        # can use it to strip it off
        base_url = re.escape(MeRESTAPIv1.get_configuration('service', 'base_url'))

        # Get the remote address
        remote_address = request.remote_addr

        MeRESTAPIv1.logger.debug(f'{remote_address} :: New request for "{path}"')
        
        try:
            # Check if the URL startes with the base URL. If it doesn't, something went terrible
            # wrong and we should raise an 'Page not found' error
            if not path.startswith(base_url):
                raise MeRESTAPIv1WrongBaseURLError('The path "{path}" does not start with the correct base URL "{base_url}"'.format(
                    path = path,
                    base_url = base_url
                ))
            
            # Get the API group and the API endpoint
            regex = '^{base_url}/([0-9a-zA-Z_+-]+)/([0-9a-zA-Z_+-]+)$'.format(
                base_url = base_url
            )
            api_parts = re.findall(regex, path)

            if len(api_parts) == 1:
                # Get the API group and the endpoint
                group, endpoint = api_parts[0]
                MeRESTAPIv1.logger.debug(f'{remote_address} :: API parts are "{api_parts[0]}"')
                
                # Now that we have the group, check if it exists
                if group in MeRESTAPIv1.registered_groups.keys():
                    try:
                        # Group exists, get the endpoints
                        endpoints = MeRESTAPIv1.registered_groups[group]['endpoints']

                        # Find the endpoint
                        if endpoint in endpoints.keys():
                            MeRESTAPIv1.logger.debug(f'{remote_address} :: Found endpoint "{endpoint}". Method: "{endpoints[endpoint]["method"]}"')
                            return endpoints[endpoint]['method']()
                        else:
                            raise MeRESTAPIv1APIEndpointNotFoundError('The API endpoint "{endpoint}" for group "{group}" does not exists'.format(
                                endpoint = endpoint,
                                group = group
                            ))
                    except KeyError as e:
                        raise MeRESTAPIv1EndpointRegistrationError(e)
                else:
                    # Didn't exist. Give an error
                    raise MeRESTAPIv1APIGroupNotFoundError('The API group "{group}" is not a valid group'.format(
                        group = group
                    ))
            else:
                raise MeRESTAPIv1InvalidAPIEndpointError('Path "{path}" is not a valid API endpoint'.format(
                    path = path
                ))
        except MeRESTAPIv1PermissionDeniedError as error:
            return MeRESTAPIv1.get_error_response(error, 403, path)
        except MeRESTAPIv1PageNotFoundError as error:
            return MeRESTAPIv1.get_error_response(error, 404, path)
        except MeRESTAPIv1ServerError as error:
            return MeRESTAPIv1.get_error_response(error, 500, path)
        except Exception as error:
            return MeRESTAPIv1.get_error_response(error, 501, path)
    
    @classmethod
    def register_group(cls, name, description):
        """ Decorator to register a API-group to this static class. To register a API, a class has
            to use this method as decorator. The decorator should be called with a name for the API
            group that is used in the API URL. The API group itself should contain a dict called
            'registered_endpoints' with the endpoints of the API.
            
            Example:
            - If the API call is for the URL '/api/v1/users/user' the following fields are defined:

                '/api/v1/' is de base_url as defined in the configuration file
                'users' is the API group
                'user'  is the API endpoint within that group. This endpoint gets registered with
                        the decorator register_endpoint
            
            By using this method to register a class as a API group, the API can be self
            documenting. This way, documentation for the complete API is not needed.
        """
        
        def decorator(class_):
            """ The real decorator method; will register the class (if the name is not already in
                use """
            
            # Check if the API group already exists. If it isn't, we create it
            if not name in cls.registered_groups.keys():
                cls.registered_groups[group] = {
                    'description': description,
                    'endpoints': dict()
                }
            else:
                MeRESTAPIv1.logger.debug(f'API group "{name}" was already registered')
                # Add the description
                cls.registered_groups[name]['description'] = description

            # After we register the group, we can return the class. If we don't do that, the class
            # will be unusable for other uses then this; it will simply stop existing in the
            # original form.
            return class_
        
        # Return the decorator
        return decorator

    @classmethod
    def register_endpoint(cls, group, name, description, permissions = None, user_token_needed = True):
        """ Decorator for API endpoints to register themselves for the application. The endpoint can
            specify what permissions are needed for the specific HTTP methods for this response. The
            permissions attribute is a dict. The keys are the specific HTTP methods that can be used
            and the values for the keys are the permissions needed for that HTTP method. Example:

            { 'GET': 'users.list', 'POST': 'users.create' }

            This would mean that that users.list permissions is needed for the client in able to 
            execute the HTTP method GET for this endpoint, and the users.create permissions are
            needed for the POST method for this endpoint.

            If 'user_token_needed' is set to False, this endpoint can be performed without a
            user-key.
        """

        # If no permissions are needed, we create an empty dict for it so we don't get any
        # TypeErrors later on
        if permissions is None:
            permissions = dict()

        def decorator(method):
            """ In the decorator, we register the endpoint in the class """

            MeRESTAPIv1.logger.debug(f'Registering endpoint "{name}" in API group "{group}"')

            # Check if the group already exists and create it if it doesn't
            if not group in cls.registered_groups.keys():
                cls.registered_groups[group] = {
                    'description': None,
                    'endpoints': dict()
                }

            # If the endpoint already exists, we raise an error
            if name in cls.registered_groups[group]['endpoints'].keys():
                raise MeRESTAPIv1EndpointAmbigiousNameError('The endpoint "{endpoint}" already exists in group "{group}"'.format(
                    endpoint = name,
                    group = group
                ))
            
            # Create a endpoint method that we use to replace the method that is being decorated
            def endpoint():
                """ The new endpoint; checks if the permissions are correct for the client and the
                    user, and if the correct methods are used """

                # Get the starting time of the endpoint so we can calculate the runtime afterwards
                starttime = time()

                # Get the remote address
                remote_address = request.remote_addr

                MeRESTAPIv1.logger.debug(f'{remote_address} :: Endpoint "{group}/{name}" started with HTTP method "{request.method.upper()}"')
                
                # --- Check the method -------------------------------------------------------------

                MeRESTAPIv1.logger.debug(f'{remote_address} :: Endpoint "{group}/{name}" checking method')

                # First, we check if the HTTP method that is being used by the client is allowed. We
                # check that by checking it against the given keys in the permissions dictionary.
                if not request.method.upper() in [ method.upper() for method in permissions.keys() ]:
                    raise MeRESTAPIv1EndpointMethodNotAllowedError('The method "{method}" is not allowed for endpoint "{endpoint}" in group "{group}"'.format(
                        method = request.method.upper(),
                        endpoint = name,
                        group = group
                    ))
                
                MeRESTAPIv1.logger.debug(f'{remote_address} :: Endpoint "{group}/{name}" was using correct method')
                
                # --- API Key check ----------------------------------------------------------------

                MeRESTAPIv1.logger.debug(f'{remote_address} :: Endpoint "{group}/{name}" checking values')

                # Then, we have to retrieve the API tokens given. There are two ways for clients to
                # pass the API token; via HTTP headers, or via the URL. If both are given, we give
                # an error since we do not allow that. We check for both the Application Token and
                # the user token, but only one of them is allowed. If a application token is given
                # and the user_token_needed is True, we raise permission denied error. If a
                # application and user token are given, we also raise a permission denied error. If
                # a user key is given and user_token_needed if False, we also give an permission
                # denied. This way, we can make sure authentication can be done savely.
                client_token_header = request.headers.get(cls.get_configuration('api', 'http_header_client_token'))
                user_token_header = request.headers.get(cls.get_configuration('api', 'http_header_user_token'))
                client_token_url = request.args.get(cls.get_configuration('api', 'http_url_client_token'))
                user_token_url = request.args.get(cls.get_configuration('api', 'http_url_user_token'))

                client_token = [ token for token in [ client_token_header, client_token_url ] if not token is None ]
                user_token = [ token for token in [ user_token_header, user_token_url ] if not token is None ]

                if len(client_token) > 1: 
                    raise MeRESTAPIv1EndpointTooManyClientTokensError('Too many client tokens tokens given. You\'re only allowed to supply a token via HTTP headers or via URL, not both!')
                elif len(client_token) == 1:
                    client_token = client_token[0]
                else:
                    client_token = None
        
                if len(user_token) > 1:
                    raise MeRESTAPIv1EndpointTooManyUserTokensError('Too many user tokens tokens given. You\'re only allowed to supply a token via HTTP headers or via URL, not both!')
                elif len(user_token) == 1:
                    user_token = user_token[0]
                else:
                    user_token = None

                # If 'user_token_needed' is set to True, we have to check if we got one user key only
                if user_token_needed:
                    if user_token is None or not client_token is None:
                        raise MeRESTAPIv1EndpointNoUserTokenGivenError('For endpoint "{endpoint}" in group "{group}" is only a user token accepted'.format(
                            method = request.method.upper(),
                            endpoint = name,
                            group = group
                        ))
                else:
                    if not user_token is None or client_token is None:
                        raise MeRESTAPIv1EndpointNoClientTokenGivenError('For endpoint "{endpoint}" in group "{group}" is only a client token accepted'.format(
                            method = request.method.upper(),
                            endpoint = name,
                            group = group
                        ))
                
                MeRESTAPIv1.logger.debug(f'{remote_address} :: Endpoint "{group}/{name}" was using correct values')

                # --- Authentication ---------------------------------------------------------------

                MeRESTAPIv1.logger.debug(f'{remote_address} :: Endpoint "{group}/{name}" authenticating')

                user_token_object = None
                client_token_object = None

                with DatabaseSession(commit_on_end = True) as session:
                    # We have a token. Now we can check if the token is valid.
                    if user_token_needed:
                        # Get the user token
                        tokens = session.query(APIUserToken).filter(APIUserToken.token == user_token)

                        # Check if we have a token, if the token isn't disabled and if it isn't
                        # expired
                        if tokens.count() == 1:
                            user_token_object = tokens.first()
                            client_token = user_token_object.client.token
                            if user_token_object.enabled:
                                if not user_token_object.expiration is None:
                                    if user_token_object.expiration < datetime.datetime.utcnow():
                                        raise MeRESTAPIv1EndpointExpiredUserTokenError('The user token "{token}" is expired'.format(
                                            token = user_token
                                        ))
                            else:
                                raise MeRESTAPIv1EndpointDisabledUserTokenError('The user token "{token}" is disabled'.format(
                                    token = user_token
                                ))
                        else:
                            raise MeRESTAPIv1EndpointNoValidUserTokenError('The user token "{token}" is not found'.format(
                                token = user_token
                            ))

                    # Get the client token
                    tokens = session.query(APIClientToken).filter(APIClientToken.token == client_token)
                    
                    # Check if we have a token, if the token isn't disabled and if it isn't
                    # expired
                    if tokens.count() == 1:
                        client_token_object = tokens.first()
                        if client_token_object.enabled:
                            if not client_token_object.expiration is None:
                                if client_token_object.expiration < datetime.datetime.utcnow():
                                    raise MeRESTAPIv1EndpointExpiredClientTokenError('The client token "{token}" is expired'.format(
                                        token = client_token
                                    ))
                        else:
                            raise MeRESTAPIv1EndpointDisabledClientTokenError('The client token "{token}" is disabled'.format(
                                token = client_token
                            ))
                    else:
                        raise MeRESTAPIv1EndpointNoValidClientTokenError('The client token "{token}" is not found'.format(
                            token = client_token
                        ))

                    MeRESTAPIv1.logger.debug(f'{remote_address} :: Endpoint "{group}/{name}" authenticated')

                    # --- Authorization ------------------------------------------------------------

                    MeRESTAPIv1.logger.debug(f'{remote_address} :: Endpoint "{group}/{name}" authorizing')

                    # Check if the application *and* the user are authorized to do this. To do this,
                    # we get the permission objects from the token-objects, but only the ones that
                    # are requested for this endpoint. We first split the requested permission in a
                    # section and a subject. But before doing that, we have to get the correct
                    # requested permission for this HTTP method
                    endpoint_permission = None
                    for methods, permission in permissions.items():
                        if methods.upper() == request.method.upper():
                            endpoint_permission = permission
                            break
                    
                    # Split the endpoint and check if it is in the correct format
                    permissions_splitted = re.findall('^([a-zA-Z0-9_-]+)\.([a-zA-Z0-9_-]+)$', endpoint_permission)
                    if len(permissions_splitted) == 1:
                        if len(permissions_splitted[0]) == 2:
                            section = permissions_splitted[0][0]
                            subject = permissions_splitted[0][1]
                        else:
                            raise MeRESTAPIv1EndpointPermissionInvalidError('Permission "{permission}" is not a valid permission string'.format(
                                permission = endpoint_permission
                            ))
                    else:
                        raise MeRESTAPIv1EndpointPermissionInvalidError('Permission "{permission}" is not a valid permission string'.format(
                            permission = endpoint_permission
                        ))

                    # We set both permissions default to False
                    client_permitted = False
                    user_permitted = False

                    # Get the client permissions
                    client_permissions = [
                        permission
                        for permission in client_token_object.client_permissions
                        if permission.granted == True and permission.permission_object.section == section and permission.permission_object.subject == subject
                    ]

                    # If we have found something, we can surely say this user is allowed to run this
                    # endpoint
                    if len(client_permissions) == 1:
                        client_permitted = True

                    # Get the user permissions
                    if user_token_needed:
                        user_permissions = [
                            permission
                            for permission in user_token_object.user_permissions
                            if permission.granted == True and permission.permission_object.section == section and permission.permission_object.subject == subject
                        ]

                        # If we have found something, we can surely say this user is allowed to run
                        # this endpoint
                        if len(user_permissions) == 1:
                            user_permitted = True
                    else:
                        # If we don't have a user_token_object, there is none because this API
                        # doesnt require a user token. We can just assume it is correct then
                        user_permitted = True
                    
                    # Check if one of them is False. If it is, we have to raise an authorization
                    # error
                    if not client_permitted:
                        raise MeRESTAPIv1EndpointClientNotAuthorizedError('The client is not authorized for "{permission}" permissions'.format(
                            permission = endpoint_permission
                        ))
                    elif not user_permitted:
                        raise MeRESTAPIv1EndpointUserNotAuthorizedError('The user is not authorized for "{permission}" permissions'.format(
                            permission = endpoint_permission
                        ))
                
                    MeRESTAPIv1.logger.debug(f'{remote_address} :: Endpoint "{group}/{name}" authorized')

                    # --- Accounting ---------------------------------------------------------------

                    MeRESTAPIv1.logger.debug(f'{remote_address} :: Endpoint "{group}/{name}" accounting')

                    # For accounting, we log the actions a client and a user do in to a database
                    # table that is designed for that specific purpose. We log the request for the
                    # client and for the user.

                    # First, we get the permissions for the token. We already got this before, so we
                    # can just reuse them
                    client_permission_id = client_permissions[0].permission
                    
                    # Create the logentry
                    client_log_entry = APIClientLogEntry(
                        client = client_token_object.id,
                        address = remote_address,
                        method = request.method.upper(),
                        api_group = group,
                        api_endpoint = name,
                        permission = client_permission_id
                    )

                    # Add the logentry
                    session.add(client_log_entry)

                    # Then we do the same for the user token; first we get the permission
                    if user_token_needed:
                        user_permission_id = user_permissions[0].permission
                    
                        # Then we create a logentry
                        user_log_entry = APIUserLogEntry(
                            user = user_token_object.user,
                            client = client_token_object.id,
                            token = user_token_object.token,
                            address = remote_address,
                            method = request.method.upper(),
                            api_group = group,
                            api_endpoint = name,
                            permission = user_permission_id
                        )

                        # Add the logentry
                        session.add(user_log_entry)

                    MeRESTAPIv1.logger.debug(f'{remote_address} :: Endpoint "{group}/{name}" accounted')

                # --- Run the real endpoint --------------------------------------------------------
                # Now that we are authenticated and authorized, we can run the method, retrieve the
                # resulting data and parse it for a good API result
                tokens = { 'user_token': user_token, 'client_token': client_token }
                return_object = method(**tokens)

                # Check if the return value is correct. If it isn't, we raise an 500 error
                if not type(return_object) is APIResponse:
                    raise MeRESTAPIv1EndpointWrongReturnTypeError('Endpoint "{endpoint}" in group "{group}" returned a "{wrong_type}" instead of a"{good_type}"'.format(
                        endpoint = name,
                        group = group,
                        wrong_type = type(return_object),
                        good_type = APIResponse
                    ))
                
                # Set the starttime. The endtime will be calculated when the result gets parsed to
                # present to the client
                return_object.starttime = starttime

                # Set the API characteristics
                return_object.api_group = group
                return_object.api_endpoint = name

                # If this response is a dataset, we might have to do some paging
                if return_object.response_type == APIResponse.TYPE_DATASET:
                    if return_object.paginate:
                        # If a page is set, we use that. Otherwise, we take the default value of 1
                        page = 1
                        if 'page' in request.args.keys():
                            try:
                                page = int(request.args['page'])
                            except ValueError:
                                raise MeRESTAPIv1EndpointPageWrongTypeError('The attribute "page" should be of type "{good_type}", not "{bad_type}"'.format(
                                    good_type = int,
                                    bad_type = type(request.args['page'])
                                ))

                        # Get the max items per page
                        items_per_page = cls.get_configuration('api', 'max_items_per_page')
                        if 'limit' in request.args.keys():
                            try:
                                items_per_page = int(request.args['limit'])
                            except ValueError:
                                raise MeRESTAPIv1EndpointLimitWrongTypeError('The attribute "limit" should be of type "{good_type}", not "{bad_type}"'.format(
                                    good_type = int,
                                    bad_type = type(request.args['limit'])
                                ))

                        # Complete the return object
                        return_object.items_per_page = items_per_page
                        return_object.page = page

                # --- Return the result ------------------------------------------------------------
                # Return the given result. If the user specified 'pretty' in the URL, we print the
                # JSON in a neet formatted way
                json_options = dict()
                if 'pretty' in request.args.keys():
                    json_options = {
                        'indent': 4,
                        'sort_keys': True
                    }
                return flask.Response(json.dumps(return_object.response, cls = MeJSONEncoder, **json_options), mimetype = 'application/json')
            
            # Add the endpoint to the group
            cls.registered_groups[group]['endpoints'][name] = {
                'method': endpoint,
                'description': description
            }

            # We return the method so it can be used
            return endpoint
        
        # Return the decorator
        return decorator
#---------------------------------------------------------------------------------------------------
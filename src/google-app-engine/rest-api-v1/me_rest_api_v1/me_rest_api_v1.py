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
from database import Database
import flask
import json
import re
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

    configfile = 'apiv1-configuration.json'
    config = None
    environment = None

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
        Database.connect(
            connection_string.format(**sql_settings),
            **cls.get_configuration(group = 'sqlalchemy')
        )
    
    @classmethod
    def start(cls):
        """ The start method start the actual application """

        # Start Flask with the configuration that is red in
        return cls.flask_app.run(**cls.get_configuration('flask'))
    
    @flask_app.route('/', defaults = { 'path': '' }, methods = [ 'GET', 'POST' ])
    @flask_app.route('/<path:path>', methods = ['GET', 'POST'])
    def api_endpoint(path):
        """ Show the correct page based on registered classes expressions """
        
        # Because we use services in Google App Engine with a dispatch.yaml file, we still have the
        # route from the dispatcher in the URL. In the configuration file, this URL is set and we
        # can use it to strip it off
        base_url = re.escape(MeRESTAPIv1.get_configuration('service', 'base_url'))
        
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
                
                # Now that we have the group, check if it exists
                if group in MeRESTAPIv1.registered_groups.keys():
                    try:
                        # Group exists, get the endpoints
                        endpoints = MeRESTAPIv1.registered_groups[group]['endpoints']

                        # Find the endpoint
                        if endpoint in endpoints.keys():
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
        except KeyboardInterrupt:
            # TODO: Decent Error Pages for the different type of Exceptions
            return 'ERROR', 500
    
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
                # Add the description
                cls.registered_groups[name]['description'] = description

            # After we register the group, we can return the class. If we don't do that, the class
            # will be unusable for other uses then this; it will simply stop existing in the
            # original form.
            return class_
        
        # Return the decorator
        return decorator

    @classmethod
    def register_endpoint(cls, group, name, description):
        """ Decorator for API endpoints to register themselves for the application """

        def decorator(method):
            """ In the decorator, we register the endpoint in the class """

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

            # Add the endpoint to the group
            cls.registered_groups[group]['endpoints'][name] = {
                'method': method,
                'description': description
            }

            # We return the method so it can be used
            return method
        
        # Return the decorator
        return decorator
#---------------------------------------------------------------------------------------------------
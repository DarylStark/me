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
    # - The 'registered_urls' will be a dictionary. The keys are going to be regular expressions
    #   that can match a specific URL to a specific class. Within this class, a method will be
    #   mapped to every specific URL and will check if there is a matching regex. If there is, the
    #   class associated with the regex will be called to show the correct page. To register a class
    #   with a regex to this, the class should use the decorator Me.register_url.
    
    flask_app = flask.Flask(__name__)
    registered_urls = {}

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
            raise MeRESTAPiv1ConfigFileError('File "{file}" doesn\'t exist'.format(file = cls.configfile))
        except json.decoder.JSONDecodeError:
            raise MeRESTAPiv1ConfigFileError('File "{file}" is not a valid JSON file'.format(file = cls.configfile))

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
                    raise MeRESTAPiv1ConfigFileError('Configuration group "{group}" does not contain a setting "{setting}"'.format(group = group, setting = setting))
            else:
                # If no setting is given, we return the complete dict for the group
                return cls.config[cls.environment][group]
        else:
            raise MeRESTAPiv1ConfigFileError('Configuration group "{group}" does not exist'.format(group = group))
    
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
    @flask_app.route('/<path:path>', methods=['GET', 'POST'])
    def show_page(path):
        """ Show the correct page based on registered classes expressions """
        
        # Because we use services in Google App Engine with a dispatch.yaml file, we still have the
        # route from the dispatcher in the URL. In the configuration file, this URL is set and we
        # can use it to strip it off
        base_url = re.escape(MeRESTAPIv1.get_configuration('service', 'base_url'))
        url = re.findall('^' + base_url + '(/.+|/)', path)

        # Check if we found something
        if len(url) == 1:
            # We search the registered groups to see if we can find a group with a regex that
            # matches this URL.
            matched_objects = list()
            for key, item in MeRESTAPIv1.registered_urls.items():
                if item['regex'].match(url[0]):
                    matched_objects.append({ 'name': key, 'item': item })
            
            # Check how many objects we found that match the url. If we have none, the page was not
            # found. If we find one, we have the page and can execute it. If we find more then one,
            # there is a ambigious regular expression and we have to present an error
            if len(matched_objects) == 0:
                # No page found
                raise MeRESTAPiv1APIGroupNotFoundError('Path "{path}" couldn\'t be found'.format(path = path))
            elif len(matched_objects) > 1:
                # Too many groups found
                raise MeRESTAPiv1APIGroupAmbigiousError('Ambigious groups found for "{path}": {groups}"'.format(
                    path = path,
                    groups = ', '.join([ '"{name}"'.format(name = x['name']) for x in matched_objects ])
                ))
            else:
                # Found just one group; perfect! We create an instance of the group and start the
                # 'page' method for it. We return the value of the start-method to Flask.
                group_instance = matched_objects[0]['item']['cls']()
                return group_instance.page(path)
        
        # Method is still running, so appearently the page string isn't prefixed with the base_url
        raise MeRESTAPiv1WrongBaseURLError('Path "{path}" is not prefixed with "{prefix}"'.format(
            path = path,
            prefix = base_url
        ))
    
    @classmethod
    def register_url(cls, regex, name, description = None):
        """ Decorator to register a URL to this static class. To register a URL, a class has to use
            this method as decorator. The decorator should be called with a regex that can match
            every URL that it should be used for and a unique name. """
        
        def decorator(class_):
            """ The real decorator method; will check if the regex is valid and register the class
                within this static class """
        
            # First, we check if the regex is valid. We do this trying to compile it. If it fails,
            # we know the regex is valid. AFAIK there is no other/better way of doing this
            try:
                compiled_regex = re.compile(regex)
            except re.error as Err:
                # Regex is not correct; raise an error
                raise MeRESTAPiv1RegistrationRegExInvalidError(Err)
            else:
                # If the regex was valid, no error is raised. We need to check if this name is
                # unique. If it isn't; thrown an error
                if name in cls.registered_urls.keys():
                    raise MeRESTAPiv1RegistrationAmbigiousNameError('There is already a registered url with name "{name}"'.format(
                        name = name
                    ))

                # We can now register the URL. We register URLs by their name. Within the dict for
                # this key we register the given compiled regular expression and the class that is
                # given.
                cls.registered_urls[name] = {
                    'regex': compiled_regex,
                    'regex_text': regex,
                    'cls': class_
                }

                # After we register the class, we can return the class. If we don't do that, the
                # class will be unusable for other uses then this; it will simply stop existing in
                # the original form.
                return class_
            
            # Return the method
            return class_
        
        # Return the decorator
        return decorator
#---------------------------------------------------------------------------------------------------
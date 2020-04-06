#!/usr/bin/env python3
"""
    me_web_gui_v1 - me_web_gui_v1.py

    Contains the main class for the Web GUI v1 part of the  application. This class, called
    MeWebGUI, can be used to run the version 1 of the Web GUI for the Me application.

    The class is meant to be run as a static class; it is impossible to create instances of it.
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me_web_gui_v1.exceptions import *
from flask import request
import flask
import logging
import datetime
import json
import re
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1:
    """ Main class for the Web GUI. Should be used as a static class """

    # Class attributes for Flask;
    # - The 'flask_app' is a class attribute that will be used as the main object for Flask. All
    #   Flask requests will be using this.
    
    flask_app = flask.Flask(__name__)

    # Class attributes;
    # - The 'configfile' is the file contains all the configuration for the application. It defaults
    #   to 'me-configuration.json', but can be changed by the calling script
    # - The 'config' will be the dict that contains the actual config.
    # - The 'environment' tells the class what environment we are in. The environment has to match a
    #   JSON key configuration file
    # - The 'starttime' is the starttime of the application (in UTC)
    # - The 'static_file_cache' is a dict that will contain static-files in a cache. This way, the
    #   files have to be retrieved from disk just one time.

    configfile = 'webv1-configuration.json'
    config = None
    environment = None
    starttime = datetime.datetime.utcnow()
    static_file_cache = dict()

    # We create a logger for application-level logging. This logger is meant to log application
    # events, not accounting details for API clients.
    logger = logging.getLogger('MeWebGUIv1')

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
            raise MeWebGUIv1ConfigFileError('File "{file}" doesn\'t exist'.format(file = cls.configfile))
        except json.decoder.JSONDecodeError:
            raise MeWebGUIv1ConfigFileError('File "{file}" is not a valid JSON file'.format(file = cls.configfile))

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
            raise MeWebGUIv1ConfigFileError('Configuration environment "{environment}" does not exist'.format(environment = environment))
    
    @classmethod
    def get_configuration(cls, group, setting = None):
        """ Returns a configuration setting for a given group (like 'database') and a given setting
            (like 'username'). If 'setting' is not given, the complete dict for the group is
            returned """
        
        # Check if a environment is set. If it isn't, we stop
        if cls.environment is None:
            raise MeWebGUIv1ConfigFileError('Environment isn\'t set! Please set environment first')

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
                    raise MeWebGUIv1ConfigFileError('Configuration group "{group}" does not contain a setting "{setting}"'.format(group = group, setting = setting))
            else:
                # If no setting is given, we return the complete dict for the group
                return cls.config[cls.environment][group]
        else:
            raise MeWebGUIv1ConfigFileError('Configuration group "{group}" does not exist'.format(group = group))
    
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

    @classmethod
    def start(cls):
        """ The start method start the actual application """

        cls.logger.info('Starting application')

        # Start Flask with the configuration that is red in
        return cls.flask_app.run(**cls.get_configuration('flask'))
    
    @flask_app.route('/', defaults = { 'path': '' }, methods = ['GET', 'POST', 'PATCH', 'DELETE'])
    @flask_app.route('/<path:path>', methods = ['GET', 'POST', 'PATCH', 'DELETE'])
    def api_endpoint(path):
        """ Show the correct page for the GUI """
        # Because we use services in Google App Engine with a dispatch.yaml file, we still have the
        # route from the dispatcher in the URL. In the configuration file, this URL is set and we
        # can use it to strip it off
        base_url = re.escape(MeWebGUIv1.get_configuration('service', 'base_url'))

        # Get the remote address
        remote_address = request.remote_addr

        MeWebGUIv1.logger.debug(f'{remote_address} :: New request for "{path}"')

        try:
            # Check if the URL startes with the base URL. If it doesn't, something went terrible
            # wrong and we should raise an 'Page not found' error
            if not path.startswith(base_url):
                raise MeWebGUIv1WrongBaseURLError('The path "{path}" does not start with the correct base URL "{base_url}"'.format(
                    path = path,
                    base_url = base_url
                ))
            
            # Get the requested page
            regex = '^{base_url}/(.+)$'.format(
                base_url = base_url
            )
            page = re.findall(regex, path)
            if len(page) == 1:
                requested_page = page[0]
                MeWebGUIv1.logger.debug(f'{remote_address} :: Requested page is "{requested_page}"')
                
                # We have the page the user wants. Let's start the correct method
                if re.match('^login/?', requested_page):
                    return MeWebGUIv1.page_login()
                else:
                    # TODO: Implement
                    return 'Unknown page. Redirect or something?'
            else:
                # TODO: Redirect the user or something?
                MeWebGUIv1.logger.debug('User didn\'t specify a page')
                return 'Redirect should be done'

        except Exception as e:
            # TODO: Custom error pages
            raise e
    
    @classmethod
    def get_static_file(cls, filetype, filename):
        """ Method to load a static file from IO and save it in the cache. The filetype specifies
            what kind of file it is; HTML, JavaScript or CSS """

        # Get the configuration for static files
        static_config = MeWebGUIv1.get_configuration('static_files')

        # Check if the filetype is correct
        if not filetype in static_config['locations'].keys():
            raise MeWebGUIv1StaticFileTypeError(f'The filetype "{filetype}" is not found')

        # Compile a string with the filename to retrieve
        full_filename = static_config['locations'][filetype] + '/' + filename

        # Check if this file is in cache, if needed
        if static_config['cache']:
            if full_filename in cls.static_file_cache.keys():
                # Found it in cache, return it immidiatly
                return cls.static_file_cache[full_filename]

        try:
            # Open the file, read its contents and return it
            with open(full_filename) as static_file:
                content = static_file.read()
            
            # If needed, put it in the cache
            if static_config['cache']:
                cls.static_file_cache[full_filename] = content
            
            # Return the content
            return content
        except FileNotFoundError:
            raise MeWebGUIStaticFileNotFoundError(f'The file "{full_filename}" cannot be found')
    
    @classmethod
    def page_login(cls):
        """ The method that returns the login-form to the user """

        # Get the login page static file
        login_page = cls.get_static_file('html', 'login.html')

        # Return the login_page
        return login_page
#---------------------------------------------------------------------------------------------------
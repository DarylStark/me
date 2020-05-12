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
from flask import Response
import flask
import logging
import datetime
import json
import re
import requests
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
    
    @flask_app.route('/', defaults = { 'path': '' }, methods = ['GET', 'POST'])
    @flask_app.route('/<path:path>', methods = ['GET', 'POST'])
    def gui_page(path):
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
                elif re.match('^js/.+$', requested_page) or re.match('^css/.+$', requested_page):
                    return MeWebGUIv1.static_page(requested_page)
                elif re.match('^client/login', requested_page):
                    return MeWebGUIv1.client_login()
                else:
                    # Nothing given, return the dashboard
                    return MeWebGUIv1.page_dashboard()
            else:
                # No page found, redirect the user to the loginpage
                MeWebGUIv1.logger.debug('User didn\'t specify a page')
                return flask.redirect('/ui/login', code = 302)
        except Exception as e:
            # Oops, a error occured. Let's display a error page
            return MeWebGUIv1.page_error(e)
    
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
            
            # Replace everything in the content that should be replaced
            replacements = {
                '{base_url}': MeWebGUIv1.get_configuration('service', 'base_url')
            }
            for key, item in replacements.items():
                content = content.replace(key, item)
            
            # If needed, put it in the cache
            if static_config['cache']:
                cls.static_file_cache[full_filename] = content
            
            # Return the content
            return content
        except FileNotFoundError:
            raise MeWebGUIStaticFileNotFoundError(f'The file "{full_filename}" cannot be found')
    
    @classmethod
    def static_page(cls, requested_page):
        """ Method to return static JavaScript and CSS files """

        # Get the requested file
        requested_file = re.findall('^(js|css)/([^\/]+)$', requested_page)

        # Check if the file matches
        if len(requested_file) == 1:
            # Get the correct filetype
            if requested_file[0][0] == 'js':
                filetype = 'javascript'
                mimetype = 'text/javascript'
            elif requested_file[0][0] == 'css':
                filetype = 'css'
                mimetype = 'text/css'
            else:
                raise MeWebGUIStaticPageNotFoundError(f'The static file "{requested_page}" cannot be found')

            # Get the static file
            try:
                static_file = cls.get_static_file(filetype, requested_file[0][1])
            except MeWebGUIStaticFileNotFoundError:
                raise MeWebGUIStaticPageNotFoundError(f'The static file "{requested_page}" cannot be found')

            # Return the static file
            return Response(static_file, mimetype = mimetype)
        else:
            raise MeWebGUIStaticPageNotFoundError(f'The static file "{requested_page}" cannot be found')

    def logged_in_page(redirect, redirect_on):
        """ Decorator for pages that require the user to be logged in. Let 'redirect' argument
            specifies if, and where the user should be redirected after the method is run. The
            'redirect_on' argument specifies when the user should be redirected: if he IS logged on,
            or if he ISN'T logged on """

        def decorator(method):
            """ The real decorator """

            def page_method(*args, **kwargs):
                """ Metod to check if a user is logged in, and to the correct task if he is or if he
                    isn't """

                # Add the full url to the redirect url
                full_url = MeWebGUIv1.get_configuration('service', 'full_url')
                redirect_url = f'{full_url}/{redirect}'

                # See if we have a user token in the cookies
                if 'user_token' in request.cookies.keys():
                    # Get the API configuration from the config
                    api_options = MeWebGUIv1.get_configuration('api')
                    api_url = f'{api_options["base_url"]}/aaa/verify_user_token'

                    # Send the API call to check if this user token is still valid
                    api_return = requests.get(url = api_url, headers = {
                        'X-Me-Auth-User': request.cookies['user_token']
                    })

                    if api_return.status_code == 200:
                        # API Return was OK. 
                        if redirect_on == 'logged_on':
                            # The user is logged in, we have to redirect him
                            return flask.redirect(redirect_url, code = 302)
                    else:
                        # API Return was NOK
                        if redirect_on == 'logged_off':
                            # The user is not logged in, we have to redirect him
                            return flask.redirect(redirect_url, code = 302)
                else:
                    # User is not logged in because there was no user key
                    if redirect_on == 'logged_off':
                        # Redirect the user
                        return flask.redirect(redirect_url, code = 302)
                
                # We made it this far; lets run the method
                return method(*args, **kwargs)
            
            # Return the new method
            return page_method
        
        # Return the decorator
        return decorator

    @logged_in_page(redirect = 'home', redirect_on = 'logged_on')
    def page_login():
        """ The method that returns the login-form to the user """

        # Get the login page static file
        login_page = MeWebGUIv1.get_static_file('html', 'login.html')

        # Return the login page
        return login_page
    
    @logged_in_page(redirect = 'login', redirect_on = 'logged_off')
    def page_dashboard():
        """ The method that returns the dashboard-application """

        # Get the dashboard page static file
        main_page = MeWebGUIv1.get_static_file('html', 'dashboard.html')

        # Return the dashboard page
        return main_page
    
    def page_error(error):
        """ The method that returns the error-page """

        # Get the error page static file
        error_page = MeWebGUIv1.get_static_file('html', 'error.html')

        # Find the error code to give
        status = 500
        if issubclass(error.__class__, MeWebGUIv1PermissionDeniedError):
            status = 403
        elif issubclass(error.__class__, MeWebGUIv1PageNotFoundError):
            status = 404

        # Return the dashboard page
        return flask.Response(error_page, status = status, mimetype = 'text/html')
    
    @classmethod
    def client_login(cls):
        """ This method is run when the user sends a POST to /client/login. The method checks tries
            to get a user_token from the API for this session and returns it. We do this in a
            Python method instead of in JavaScript so the client is not obligated to make his
            client token publically available """
        
        if request.method == 'POST':
            # Get the given username and password
            json_data = request.json

            # Check if the needed values are given
            if not 'username' in json_data.keys() or not 'password' in json_data.keys():
                raise MeWebGUIv1LoginUsernameOrPasswordNotSpecifiedError('Username or password not specified in request')

            # Check if the values are filled in
            if json_data['username'] in (None, '') or json_data['password'] in (None, ''):
                raise MeWebGUIv1LoginUsernameOrPasswordNotSpecifiedError('Username or password were empty in request')
                
            # Alright, we have the correct values. Let's retrieve a user token. To do this, we first
            # have to gather some information about the API;
            api_options = cls.get_configuration('api')
            api_url = f'{api_options["base_url"]}/aaa/retrieve_user_token_with_credentials'

            # Create the data for the API
            api_data = {
                'username': json_data['username'],
                'password': json_data['password']
            }

            # If the user supplied a 2nd-token, we can add it to the data
            if 'second_factor' in json_data.keys():
                api_data['2nd_factor'] = json_data['second_factor']

            # Do the actual POST request to the api
            api_return = requests.post(url = api_url, json = api_data, headers = {
                'X-Me-Auth-Client': api_options['api_token']
            })

            # Check the response code
            if api_return.status_code == 403:
                raise MeWebGUIv1LoginFailedError('Login failed; credentials are wrong')
            elif api_return.status_code != 200:
                raise MeWebGUIv1LoginAPIResponseError(f'API responded with code {api_return.status_code} and data: {api_return.json()}')

            # Looks like everything went fine. Check the response
            response_json = api_return.json()
            if response_json['object']['_type'] == '2nd_factor':
                # User needs to supply a second factor
                return_object = { '2nd_factor_required': True }
            elif response_json['object']['_type'] == 'api_user_token':
                # We have a valid user token. Let's use it!
                return_object = { 'user_token': response_json['object']['token'] }

            # Return the result to the Web UI
            return flask.Response(json.dumps(return_object), mimetype = 'application/json')
        else:
            raise MeWebGUIClientWrongMethodError(f'Method "{request.method}" is not accepted')
#---------------------------------------------------------------------------------------------------
#!/usr/bin/python3
"""
    Main entry point for the application. Supposed to be ran as script or by Google App Engine
"""
#---------------------------------------------------------------------------------------------------
# Imports
from me_web_gui_v1 import MeWebGUIv1
import logging
#---------------------------------------------------------------------------------------------------
# First, we make sure the configuration gets loaded
MeWebGUIv1.load_config()

# Then, we can set the environment
MeWebGUIv1.set_environment('development')

# We check if the '__name__' variable contains the string '__main__'. If it does, we are running
# this as a script and therefor on the development server.
if __name__ == '__main__':
    # Configure the logging module
    logging.basicConfig(**MeWebGUIv1.get_configuration('logging'))

    # Next, we can initiate the application. What this does, is creating a database connection
    # and making sure all needed tables exsist
    MeWebGUIv1.initiate()

    # Start the application. We only need to do this on the development server; the Google App
    # Engine environment will start the application directly from the Flask-object in the Me class.
    MeWebGUIv1.start()
else:
    # We are not running on the development server. Let's set the enviroment to 'production' so the
    # application can use the correct values.
    MeWebGUIv1.set_environment('production')

    # Configure the logging module
    logging.basicConfig(**MeWebGUIv1.get_configuration('logging'))

    # Initiate the application
    MeWebGUIv1.initiate()

    # Set the 'app' environment variable for Google App Engine
    app = MeWebGUIv1.flask_app
#---------------------------------------------------------------------------------------------------
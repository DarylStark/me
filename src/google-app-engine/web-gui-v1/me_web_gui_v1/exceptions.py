"""
    me_web_gui_v1 - exceptions
    Author: Daryl Stark

    Module with custom exceptions for 'me_web_gui_v1'
"""
#---------------------------------------------------------------------------------------------------
# Bases classes for Exceptions. These define what kind of error-page is displayed when a error
# happends.
#---------------------------------------------------------------------------------------------------
class MeWebGUIError(Exception):
    """ Base exception for MeWebGUI-exceptions """
    pass
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1CriticalError(MeWebGUIError):
    """ Exception that should result in complete termination of the application """
    pass
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1PermissionDeniedError(MeWebGUIError):
    """ Base exception for 403-errors """
    pass
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1PageNotFoundError(MeWebGUIError):
    """ Base exception for 404-errors """
    pass
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1ServerError(MeWebGUIError):
    """ Base exception for 500-errors """
    pass
#---------------------------------------------------------------------------------------------------
# Critical errors; errors that should stop the complete application
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1ConfigFileError(MeWebGUIv1CriticalError):
    """ Error that happends when something goes wrong with the configfile. The file is either not
        a valid configfile, or the file doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
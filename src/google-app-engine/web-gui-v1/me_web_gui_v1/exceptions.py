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
class MeWebGUIv1FirestoreInitiationError(MeWebGUIv1CriticalError):
    """ Error that gets raised when Firestore cannot be initiated """
    pass
#---------------------------------------------------------------------------------------------------
# PageNotFoundErrors: errors that happen when a page or resource is requested that doesn't exists
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1WrongBaseURLError(MeWebGUIv1PageNotFoundError):
    """ Error when the user opens a URL that doesn't start with the right base_url """
    pass
#---------------------------------------------------------------------------------------------------
class MeWebGUIStaticPageNotFoundError(MeWebGUIv1PageNotFoundError):
    """ Error when the user opens a static page that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeWebGUIClientWrongMethodError(MeWebGUIv1PageNotFoundError):
    """ Error when the user tries to open the /client-url with a wrong HTTP method """
    pass
#---------------------------------------------------------------------------------------------------
# PermissionDeniedErrors: errors that happen when a user is not authorized to open a specific page
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1LoginUsernameOrPasswordNotSpecifiedError(MeWebGUIv1PermissionDeniedError):
    """ Error when the user tries to login without a username or password """
    pass
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1LoginFailedError(MeWebGUIv1PermissionDeniedError):
    """ Error when the user tries to login with a wrong username or password """
    pass
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1ClientUserSettingsNoTokenError(MeWebGUIv1PermissionDeniedError):
    """ Error when the user tries to retrieve user settings without a token """
    pass
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1ClientUserSettingsInvalidTokenError(MeWebGUIv1PermissionDeniedError):
    """ Error when the user tries to retrieve user settings with a invalid token """
    pass
#---------------------------------------------------------------------------------------------------
# ServerErrors: errors that happen on the server and that are not the users fault
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1StaticFileTypeError(MeWebGUIv1ServerError):
    """ Error when a static file type is not correct """
    pass
#---------------------------------------------------------------------------------------------------
class MeWebGUIStaticFileNotFoundError(MeWebGUIv1ServerError):
    """ Error when a static file is not found """
    pass
#---------------------------------------------------------------------------------------------------
class MeWebGUIv1LoginAPIResponseError(MeWebGUIv1ServerError):
    """ Error when the API responds with something else then '200' """
    pass
#---------------------------------------------------------------------------------------------------
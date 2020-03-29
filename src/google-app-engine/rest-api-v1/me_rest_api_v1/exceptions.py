"""
    me_rest_api_v1 - exceptions
    Author: Daryl Stark

    Module with custom exceptions for 'me_rest_api_v1'
"""
#---------------------------------------------------------------------------------------------------
# Bases classes for Exceptions. These define what kind of error-page is displayed when a error
# happends.
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1Error(Exception):
    """ Base exception for MeRESTAPI-exceptions """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1CriticalError(MeRESTAPIv1Error):
    """ Exception that should result in complete termination of the application """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1PermissionDeniedException(MeRESTAPIv1CriticalError):
    """ Base exception for 403-errors """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1PageNotFoundError(MeRESTAPIv1CriticalError):
    """ Base exception for 404-errors """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1ServerError(MeRESTAPIv1CriticalError):
    """ Base exception for 500-errors """
    pass
#---------------------------------------------------------------------------------------------------
# Critical errors; errors that should stop the complete application
#---------------------------------------------------------------------------------------------------
class MeRESTAPiv1ConfigFileError(MeRESTAPIv1CriticalError):
    """ Error that happends when something goes wrong with the configfile. The file is either not
        a valid configfile, or the file doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPiv1RegistrationRegExInvalidError(MeRESTAPIv1CriticalError):
    """ Exception when the application tries to register a API group with a invalid regex """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPiv1RegistrationAmbigiousNameError(MeRESTAPIv1CriticalError):
    """ Exception when the application tries to register a API group with a name that already is
        registered """
    pass
#---------------------------------------------------------------------------------------------------
# PageNotFoundErrors: errors that happen when a page or resource is requested that doesn't exists
#---------------------------------------------------------------------------------------------------
class MeRESTAPiv1WrongBaseURLError(MeRESTAPIv1PageNotFoundError):
    """ Error when the user opens a URL that doesn't start with the right base_url """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPiv1APIGroupNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error for when the user tries to open an API group that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
# Server Errors: errors that happen on the server and that are not the users fault
#---------------------------------------------------------------------------------------------------
class MeRESTAPiv1APIGroupAmbigiousError(MeRESTAPIv1ServerError):
    """ When the API notices a URL can be matched with two or more registered groups """
    pass
#---------------------------------------------------------------------------------------------------
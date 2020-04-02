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
class MeRESTAPIv1PermissionDeniedError(MeRESTAPIv1Error):
    """ Base exception for 403-errors """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1PageNotFoundError(MeRESTAPIv1Error):
    """ Base exception for 404-errors """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1ServerError(MeRESTAPIv1Error):
    """ Base exception for 500-errors """
    pass
#---------------------------------------------------------------------------------------------------
# Critical errors; errors that should stop the complete application
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1ConfigFileError(MeRESTAPIv1CriticalError):
    """ Error that happends when something goes wrong with the configfile. The file is either not
        a valid configfile, or the file doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointAmbigiousNameError(MeRESTAPIv1CriticalError):
    """ Exception when the application tries to register a API endpoint with a name that already is
        registered for this specific group """
    pass
#---------------------------------------------------------------------------------------------------
# PageNotFoundErrors: errors that happen when a page or resource is requested that doesn't exists
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1WrongBaseURLError(MeRESTAPIv1PageNotFoundError):
    """ Error when the user opens a URL that doesn't start with the right base_url """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1InvalidAPIEndpointError(MeRESTAPIv1PageNotFoundError):
    """ Error when the user specifies a invalid enpoint """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1APIGroupNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error for when the user tries to open an API group that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1APIEndpointNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error for when the user tries to open an API endpoint that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
# PermissionDeniedErrors: errors that happen on the server and that are not the users fault
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointMethodNotAllowedError(MeRESTAPIv1PermissionDeniedError):
    """ Error when the user tries to use a HTTP method that is not allowed for the specific endpoint
    """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointTooManyClientTokensError(MeRESTAPIv1PermissionDeniedError):
    """ Error when the user supplies two client tokens """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointTooManyUserTokensError(MeRESTAPIv1PermissionDeniedError):
    """ Error when the user supplies to user tokens """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointNoUserTokenGivenError(MeRESTAPIv1PermissionDeniedError):
    """ Error when a user tries to execute a endpoint without a user key while this is required """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointNoClientTokenGivenError(MeRESTAPIv1PermissionDeniedError):
    """ Error when a user tries to execute a endpoint with a client key while this is required """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointNoValidClientTokenError(MeRESTAPIv1PermissionDeniedError):
    """ Error when the user specifies a non-existing client token """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointDisabledClientTokenError(MeRESTAPIv1PermissionDeniedError):
    """ Error when the user specifies a disabled client token """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointExpiredClientTokenError(MeRESTAPIv1PermissionDeniedError):
    """ Error when the user specifies a expired client token """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointNoValidUserTokenError(MeRESTAPIv1PermissionDeniedError):
    """ Error when the user specifies a non-existing user token """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointDisabledUserTokenError(MeRESTAPIv1PermissionDeniedError):
    """ Error when the user specifies a disabled user token """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointExpiredUserTokenError(MeRESTAPIv1PermissionDeniedError):
    """ Error when the user specifies a expired user token """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointClientNotAuthorizedError(MeRESTAPIv1PermissionDeniedError):
    """ Error when a client token isn't authorized for a specific endpoint """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointUserNotAuthorizedError(MeRESTAPIv1PermissionDeniedError):
    """ Error when a user token isn't authorized for a specific endpoint """
    pass
#---------------------------------------------------------------------------------------------------
# ServerErrors: errors that happen on the server and that are not the users fault
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointRegistrationError(MeRESTAPIv1ServerError):
    """ Error for when a endpoint-object is not valid """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointPermissionInvalidError(MeRESTAPIv1ServerError):
    """ Error that happens when a endpoint has a invalid permission value """
    pass
#---------------------------------------------------------------------------------------------------
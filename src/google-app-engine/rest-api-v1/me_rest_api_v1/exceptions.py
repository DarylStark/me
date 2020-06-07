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
class MeRESTAPIv1EndpointPageWrongTypeError(MeRESTAPIv1PageNotFoundError):
    """ Error when a endpoint get a page that isn't a integer """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointLimitWrongTypeError(MeRESTAPIv1PageNotFoundError):
    """ Error when a endpoint get a page that isn't a integer """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointInvalidPageError(MeRESTAPIv1PageNotFoundError):
    """ Error when a endpoint get a invalid page """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAAChangePasswordMissingFieldsError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to change his password and fields are missing """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAAUpdateUserTokenMissingIDError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to update a user token with a missing ID """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAAUpdateUserTokenMissingNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to update a user token that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAACreateUserTokenMissingClientIDError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to create a user token without a client ID """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAACreateUserTokenClientNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to create a user token for a client that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAADeleteUserTokenMissingNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to update a user token that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AADeleteUserTokenMissingIDError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to delete a user token with a missing ID """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAASetTokenDescriptionMissingDescriptionError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to set a description for the current token without a new description
    """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1APIClientUpdateClientTokenMissingIDError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to update a client token with a missing ID """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1APIClientUpdateClientTokenNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to update a client token that doesn't exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAAUserPermissionsNotAllFieldsError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to retrieve update a User API permissions without specifying all the
        needed options """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAAUserPermissionsTokenNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to retrieve User API permissions for a token that doesn't exists or
        is not his """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAAUserPermissionsPermissionNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to update a API User Permissions for a permission that doesn't
        exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1APIClientsPermissionsNotAllFieldsError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to retrieve updata a Client API permissions without specifying all the
        needed options """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1APIClientsPermissionsTokenNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to retrieve client API permissions for a token that doesn't exists
    """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1APIClientsPermissionsPermissionNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to update a API Client Permissions for a permission that doesn't
        exist """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1APIClientsCreateClientTokenMissingFieldsError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to create a API client without specifing all the fields """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1APIClientDeleteClientTokenMissingIDError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to delete a API client without specifing the id """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1APIClientDeleteClientTokenMissingNotFoundError(MeRESTAPIv1PageNotFoundError):
    """ Error when a user tries to delete a API client that doesn't exist """
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
class MeRESTAPIv1AAARetrieveUserTokenNoDataError(MeRESTAPIv1PermissionDeniedError):
    """ Error when a user tries to retrieve a user token without providing (correct) information """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAARetrieveUserTokenUserNotFoundError(MeRESTAPIv1PermissionDeniedError):
    """ Error when a user tries to retrieve a user token with a wrong username """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAARetrieveUserTokenPasswordWrongError(MeRESTAPIv1PermissionDeniedError):
    """ Error when a user tries to retrieve a user token with a wrong password """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAARetrieveUserTokenFactorWrongError(MeRESTAPIv1PermissionDeniedError):
    """ Error when a user tries to retrieve a user token with a wrong 2nd factor code """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAAVerifyTwoFactorMissingFieldsError(MeRESTAPIv1PermissionDeniedError):
    """ Error when a user tries to verify a second factor without a code """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAAEnableTwoFactorAlreadyEnabledError(MeRESTAPIv1PermissionDeniedError):
    """ Error when a user tries to verify a second factor for a account where second factor is
        already enabled """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAAVerifyTwoFactorAlreadyEnabledError(MeRESTAPIv1PermissionDeniedError):
    """ Error when a user tries to verify a second factor for a account where second factor is
        already enabled """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AAAUpdateUserTokenWrongFieldFormatError(MeRESTAPIv1PermissionDeniedError):
    """ Error for when a user tries to update the expire field for a user token with a invalid date
    """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AARefreshUserTokenInfiniteTokenError(MeRESTAPIv1PermissionDeniedError):
    """ Error for when a user tries to refresh a user token that has a infinite expire date """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1AARefreshUserTokenNotExpiringYetTokenError(MeRESTAPIv1PermissionDeniedError):
    """ Error for when a user tries to refresh a user token that is not about to expire """
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
class MeRESTAPIv1EndpointWrongReturnTypeError(MeRESTAPIv1ServerError):
    """ Error when a endpoint returns a wrong return type """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointWrongResponseTypeError(MeRESTAPIv1ServerError):
    """ Error when a endpoint returns a wrong respsone type """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointDataNotAListError(MeRESTAPIv1ServerError):
    """ Error when a endpoint returns data that isn't a list """
    pass
#---------------------------------------------------------------------------------------------------
class MeRESTAPIv1EndpointDataNotABoolError(MeRESTAPIv1ServerError):
    """ Error when a endpoint returns data that isn't a boolean """
    pass
#---------------------------------------------------------------------------------------------------
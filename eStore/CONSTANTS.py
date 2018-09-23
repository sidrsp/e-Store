import os

class CONSTANTS:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_FOLDER='./templates/new_tmpls'
    STATIC_URL_PATH='/eStore/static'

    print('PROJECT_ROOT : ' + str(PROJECT_ROOT))


class API_RESPONSE_CODES:

    '''

    1xx: Informational	Communicates transfer protocol-level information.
    2xx: Success	Indicates that the client’s request was accepted successfully.
    3xx: Redirection	Indicates that the client must take some additional action in order to complete their request.
    4xx: Client Error	This category of error status codes points the finger at clients.
    5xx: Server Error	The server takes responsibility for these error status codes.

    '''

    SUCCESS_STATUS_CODE = 200
    CREATED_STATUS_CODE = 201
    NO_CONTENT_STATUS_CODE = 204

    BAD_REQUEST_ERROR_STATUS_CODE = 400
    UNAUTHORIZED_ERROR_STATUS_CODE = 401
    FORBIDDEN_SERVER_ERROR_STATUS_CODE = 403
    NOTFOUND_ERROR_STATUS_CODE = 404
    UNSUPPORTED_MEDIATYPE_ERROR_STATUS_CODE = 415

    INTERNAL_SERVER_ERROR_STATUS_CODE = 500


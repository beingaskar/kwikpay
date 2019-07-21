from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """ Custom exception handler used to provide exception response in generic
    format across service.
    """

    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'data': {},
            'status': False,
            'error_msg': str(exc)
        }

    return response

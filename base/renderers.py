from rest_framework.response import Response
from rest_framework import status


def custom_response_renderer(
        data=None, error_msg=None, status=None,
        status_code=status.HTTP_200_OK):
    """ Renderer to perform rendering of API response in generic format across
    the service.
    """

    return Response(
        {
            "status": status,
            "data": data,
            "error_msg": error_msg
        },
        status=status_code
    )

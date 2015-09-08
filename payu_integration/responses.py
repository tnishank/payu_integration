# Third-Party imports
from rest_framework import status
from rest_framework.response import Response


def _send_response(response_data, response_code):
    response_data.update({"status": response_code})
    return Response(response_data, status=response_code)


def send_200(reponse_data):
    return _send_response(reponse_data, status.HTTP_200_OK)

def send_400(response_data):
    return _send_response(response_data, status.HTTP_400_BAD_REQUEST)

def send_422(response_data):
    return _send_response(response_data, 422)
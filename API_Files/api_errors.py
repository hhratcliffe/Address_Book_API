"""API Error Handling

This file contains basic error handling methods use within my API. The methods are to make errors easier for users to understand.

"""
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
  """
  Returns an HTTP status error and an error message, formatted in JSON

  Parameters
  ----------
  status_code: int
    HTTP status code to indicate type of error
  message: str
    The error message to be displayed (default is None)
  """
  payload = {'error': str(status_code)+" : "+HTTP_STATUS_CODES.get(status_code, "Unknown Error")}
  if message:
    payload['message'] = message
  response = jsonify(payload)
  response.status_code = status_code
  return response


def bad_request(message):
  """
  Returns a 400 Bad Request error, accompanied by the provided message
  Included due to a majority of error messages needing to be returned as 400 Bad Request errors

  Parameters
  ----------
  message: str
    The error message to be displayed
  """
  return error_response(400, message)

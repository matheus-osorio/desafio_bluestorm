from flask import Response
import json
from typing import Union

def parse_headers(req: dict) -> dict:
  header = {}

  for content in req:
    name, data = content
    header[name.lower().replace('-','_')] = data
  
  return header


def respond(status: int, message: Union[str, dict]) -> Response:
  if type(message) != str:
    message = json.dumps(message)

  response = Response(status=status)
  response.set_data(message)

  return response
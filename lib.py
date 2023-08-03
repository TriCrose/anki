"""
Logic concerning Anki interactions via the AnkiConnect HTTP server.
"""


# std lib
import http
import json
from typing import Dict, Any

# third party
import requests


ENDPOINT_URL = "http://localhost:8765/"


class AnkiError(Exception):
    pass

class BadResponse(AnkiError):
    pass

class InternalError(AnkiError):
    pass


def anki(action, **params) -> Any:
    req = {'action': action, 'params': params, 'version': 6}
    req_json = json.dumps(req).encode('utf-8')
    res = requests.post(ENDPOINT_URL, data=req_json)
    if res.status_code != http.HTTPStatus.OK:
        raise BadResponse(f"Server returned {res.status_code} {res.reason}")
    res_json = res.json()

    if len(res_json) != 2:
        raise BadResponse(f"Invalid number of fields in reponse: {res_json=}")
    if "error" not in res_json:
        raise BadResponse(f"No 'error' field in response: {res_json=}")
    if "result" not in res_json:
        raise BadResponse(f"No 'result' field in response: {res_json=}")
    if res_json["error"] is not None:
        raise InternalError(f"Unexpected error: {res_json=}")

    return res_json["result"]

import json
from http import HTTPStatus
from bottle import response

def json_response(payload: dict, status_code: HTTPStatus = HTTPStatus.OK) -> str:
    '''
    Prepares a stringified JSON response object based on the given payload.
    If not status_code is given then '200 OK' is assumed.
    '''
    response.headers['Content-Type'] = 'application/json'
    response.status = status_code
    return json.dumps(payload)


def error_response(reason: str, status_code: HTTPStatus) -> str:
    '''
    Prepares a stringified JSON response to notify errors or exceptions.
    A descriptive 'reason' message and a corresponding 'HTTP status' are required.
    '''
    return json_response(
        payload={
            'status': status_code,
            'reason': reason
        },
        status_code=status_code
    )

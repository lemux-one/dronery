import json
from http import HTTPStatus
from bottle import response


def json_response(
        payload: dict, 
        status_code: HTTPStatus
    ) -> str:
    '''
    Prepares a stringified JSON response object.
    '''
    response.headers['Content-Type'] = 'application/json'
    response.status = status_code
    return json.dumps(payload)


def data_response(
        data: dict, 
        status_code: HTTPStatus = HTTPStatus.OK
    ) -> str:
    '''
    Prepares a stringified JSON response to wrap data.
    '''
    return json_response(
        payload={
            'status': status_code,
            'data': data
        }, 
        status_code=status_code
    )


def error_response(
        reason: str = 'Internal server error', 
        status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    ) -> str:
    '''
    Prepares a stringified JSON response to notify errors or exceptions.
    '''
    return json_response(
        payload={
            'status': status_code,
            'reason': reason
        },
        status_code=status_code
    )

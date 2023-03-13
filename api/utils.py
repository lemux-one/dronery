import json
from http import HTTPStatus
from bottle import (
    response,
    request
)
from datetime import datetime


class ApiError(Exception):
    def __init__(self, 
            status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
            message: str = 'Unexpected error'
        ):
        self.status_code = status_code
        self.message = message
        if self.status_code >= 500:
            log(self.message, 'ERROR')


def log(message: str, level: str = 'INFO'):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{level}] | {now} | {message}')


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


def extract_payload() -> dict:
    if request.content_type != 'application/json':
        abort(HTTPStatus.BAD_REQUEST, 'Only json-formatted payload accepted')
    try:
        return request.json
    except JSONDecodeError as ex:
        log(str(ex), 'ERROR')
        abort(HTTPStatus.BAD_REQUEST, 'Invalid json')


def truncate_str(long_str: str, max_len: int = 100, suffix: str = '...') -> str:
    trimmed = long_str.split('\n')[0]
    if len(trimmed) + 1 < len(long_str):
        trimmed += suffix
    elif len(trimmed) > max_len:
        trimmed = trimmed[:max_len] + suffix
    return trimmed
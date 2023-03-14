from http import HTTPStatus
from json import JSONDecodeError
from bottle import (
    abort,
    request,
    response,
    auth_basic
)
from api.api_bottle import ApiBottle
from api.utils import (
    data_response,
    error_response,
    log,
    extract_payload
)
from api.services import medications_service as service
from auth.basic import check_credentials

model = service.model

#
# Handle routes
#
handler = ApiBottle()

@handler.get('/')
def handle_list():
    '''
    Lists existing records
    '''
    filters_query = request.query.decode()
    return data_response(service.get_all_records(filters_query))


@handler.post('/')
@auth_basic(check_credentials)
def handle_create():
    '''
    Creates a new record with the given data
    '''
    payload = extract_payload()
    rowid = service.insert_record(payload)
    response.headers['Location'] = request.fullpath + str(rowid)
    return data_response({}, status_code=HTTPStatus.CREATED)


@handler.get('/<id:int>')
def handle_details(id):
    '''
    Shows details for the record matching given ID.
    '''
    return data_response(service.get_record_by_id(id))


@handler.put('/<id:int>')
@auth_basic(check_credentials)
def handle_update(id):
    '''
    Replaces data for the record matching given ID.
    '''
    payload = extract_payload()
    service.update_record_by_id(id, payload)
    return data_response({}, status_code=HTTPStatus.NO_CONTENT)


@handler.delete('/<id:int>')
@auth_basic(check_credentials)
def handle_delete(id):
    '''
    Deletes record matching given ID.
    '''
    service.delete_by_id(id)
    return data_response({})
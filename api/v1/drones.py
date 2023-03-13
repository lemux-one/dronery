from http import HTTPStatus
from json import JSONDecodeError
from bottle import (
    abort,
    request,
    response
)
from api.api_bottle import ApiBottle
from api.utils import (
    data_response,
    error_response,
    log,
    extract_payload
)
from db.sqlite import helper
from db.model import Model, Field
from db.service import Service


#
# Data model
#
'''
A Drone has:
- serial number (100 characters max);
- model (Lightweight, Middleweight, Cruiserweight, Heavyweight);
- weight limit (500gr max);
- battery capacity (percentage);
- state (IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING)
'''
model = Model(table='drones')
model.add_field(Field(name='drone_id', dtype=Field.INTEGER_TYPE, pk=True))
model.add_field(Field(name='serial_number', dtype=Field.VARCHAR_TYPE, 
    max=100, unique=True))
model.add_field(Field(name='model', dtype=Field.SELECT_TYPE, 
    options=['Lightweight', 'Middleweight', 'Cruiserweight', 'Heavyweight']))
model.add_field(Field(name='weight_limit', dtype=Field.INTEGER_TYPE, 
    min=0, max=500))
model.add_field(Field(name='battery_capacity', dtype=Field.INTEGER_TYPE, 
    min=0, max=100))
model.add_field(Field(name='state', dtype=Field.SELECT_TYPE, 
    options=['IDLE', 'LOADING', 'LOADED', 'DELIVERING', 'DELIVERED', 'RETURNING']))

service = Service(dbhelper=helper, model=model)


#
# Handle routes
#
handler = ApiBottle()

@handler.get('/')
def handle_list():
    '''
    Lists existing records
    '''
    return data_response(service.get_all_records())


@handler.post('/')
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
def handle_update(id):
    '''
    Replaces data for the record matching given ID.
    '''
    payload = extract_payload()
    service.update_record_by_id(id, payload)
    return data_response({}, status_code=HTTPStatus.NO_CONTENT)


@handler.delete('/<id:int>')
def handle_delete(id):
    '''
    Deletes record matching given ID.
    '''
    service.delete_by_id(id)
    return data_response({})
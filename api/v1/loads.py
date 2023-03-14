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
from .drones import service as drones_service
from .medications import service as medications_service


#
# Data model
#
'''
A Load has:
- drone_id (FK);
- medication_id (FK).
- quantity (how many units of the medication);
'''
model = Model(table='loads')
model.add_field(Field(name='load_id', dtype=Field.INTEGER_TYPE, pk=True))
model.add_field(Field(name='drone_id', dtype=Field.INTEGER_TYPE, 
    fk=True, ftable='drones'))
model.add_field(Field(name='medication_id', dtype=Field.INTEGER_TYPE, 
    fk=True, ftable='medications'))
model.add_field(Field(name='quantity', dtype=Field.INTEGER_TYPE, min=0))

service = Service(dbhelper=helper, model=model)

def __check_drone_constraints(drone: dict):
    # check that battery level is above 25%
    if drone['battery_capacity'] < 25:
        abort(HTTPStatus.CONFLICT, 'Low battery')
    
    # chck state is "IDLE" or "LOADING"
    if drone['state'] not in ('IDLE', 'LOADING'):
        abort(HTTPStatus.CONFLICT, 'Drone unavailable')

    medication = medications_service.get_record_by_id(model.obj['medication_id'])
    meds = medications_service.get_all_records()
    
    # take only the relevant loads
    loads = service.get_all_records()
    loads = [load for load in loads if load['drone_id'] == drone['drone_id']]
    
    # get total load weight and check if the new load will not exceed the weight limit
    total_weight = 0
    for load in loads:
        meds_in_load = [med for med in meds if med['medication_id'] == load['medication_id']]
        for med in meds_in_load:
            total_weight += med['weight'] * load['quantity']
    load_weight = medication['weight'] * model.obj['quantity']
    if total_weight + load_weight > drone['weight_limit']:
        abort(HTTPStatus.CONFLICT, 'Load exceeds weight limit')

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
def handle_create():
    '''
    Creates a new record with the given data
    '''
    payload = extract_payload()
    try:
        model.from_dict(payload)
    except ValueError as ex:
        abort(HTTPStatus.BAD_REQUEST, str(ex))
    for field in model.fields:
        service.check_constraints(field)
    
    drone = drones_service.get_record_by_id(payload['drone_id'])
    __check_drone_constraints(drone)
    
    rowid = service.insert_record(payload)
    drone['state'] = 'LOADING'
    drones_service.update_record_by_id(drone['drone_id'], drone)
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
    try:
        model.from_dict(payload)
    except ValueError as ex:
        abort(HTTPStatus.BAD_REQUEST, str(ex))
    for field in model.fields:
        service.check_constraints(field)
    
    drone = drones_service.get_record_by_id(payload['drone_id'])
    __check_drone_constraints(drone)

    service.update_record_by_id(id, payload)
    drone['state'] = 'LOADING'
    drones_service.update_record_by_id(drone['drone_id'], drone)
    return data_response({}, status_code=HTTPStatus.NO_CONTENT)


@handler.delete('/<id:int>')
def handle_delete(id):
    '''
    Deletes record matching given ID.
    '''
    service.delete_by_id(id)
    return data_response({})
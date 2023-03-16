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
from api.services import loads_service as service
from api.services import drones_service
from api.services import medications_service

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


#
#   Utilties
#
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


handler.HELP = '''
<div>
<ul>
    <li>
        <details>
            <summary>GET /loads</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X GET 'http://127.0.0.1:8080/api/v1/loads'
                </pre>
                <h4>Response</h4>
                <pre>
{
    "status": 200,
    "data": [
        {
            "load_id": 1,
            "drone_id": 2,
            "medication_id": 1,
            "quantity": 2
        },
        ...
    ]
}
                </pre>
                <details>
                    <summary>Filtering</summary>
                    <div>
                        <h4>Optional parameters to filter the results</h4>
                        <p>To enable filtering append a query part to the endpoint with the following strutcture:</p>
                        <pre>
?field=[operator]value[,value2,...][&field=[operator]value[,value2,...]]
                        </pre>
                        <p>Where:</p>
                        <ul>
                            <li>"field" can be any of the object's attributes</li>
                            <li>the [ ] represents optional elements</li>
                            <li>"operator" can be one of ('=', '<=', '>=', '<>', '!=', '<', '>', 'in') with '=' as default if not especified</li>
                        </ul>
                        <p>For instance:</p>
                        <pre>
?quantity=[>]10
                        </pre>
                    </div>
                </details>
            </div>
        </details>
    </li>
    
    <li>
        <details>
            <summary>POST /loads</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X POST 'http://127.0.0.1:8080/api/v1/loads/'
--header 'Authorization: Basic YWRtaW46YWRtaW4='
--header 'Content-Type: application/json'
--data-raw '{
    "drone_id": 1,
    "medication_id": 1,
    "quantity": 1
}'
                </pre>
                <h4>Response</h4>
                <pre>
HEADER Location: /api/v1/loads/4
{
    "status": 201,
    "data": {}
}
                </pre>
            </div>
        </details>
    </li>

    <li>
        <details>
            <summary>GET /loads/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X GET 'http://127.0.0.1:8080/api/v1/loads/1'
                </pre>
                <h4>Response</h4>
                <pre>
{
    "status": 200,
    "data": {
        "load_id": 1,
        "drone_id": 2,
        "medication_id": 1,
        "quantity": 2
  }
}
                </pre>
            </div>
        </details>
    </li>

    <li>
        <details>
            <summary>PUT /loads/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X PUT 'http://127.0.0.1:8080/api/v1/loads/1'
--header 'Authorization: Basic YWRtaW46YWRtaW4='
--header 'Content-Type: application/json'
--data-raw '{
    "drone_id": 1,
    "medication_id": 1,
    "quantity": 1
}'
                </pre>
                <h4>Response</h4>
                <pre>
HTTP 204 No Content
                </pre>
            </div>
        </details>
    </li>

    <li>
        <details>
            <summary>DELETE /loads/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X DELETE 'http://127.0.0.1:8080/api/v1/loads/4'
                </pre>
                <h4>Response</h4>
                <pre>
{
    "status": 200,
    "data": {}
}
                </pre>
            </div>
        </details>
    </li>

</ul>
</div>
'''
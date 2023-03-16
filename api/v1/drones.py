from http import HTTPStatus
from bottle import (
    abort,
    request,
    response,
    auth_basic,
    MultiDict
)
from api.api_bottle import ApiBottle
from api.utils import (
    data_response,
    error_response,
    log,
    extract_payload
)
from api.services import drones_service as service
from auth.basic import check_credentials
from api.services import loads_service
from api.services import medications_service

FLEET_CAPACITY = 10
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
    drones = service.get_all_records()
    if len(drones) >= FLEET_CAPACITY:
        abort(HTTPStatus.CONFLICT, 'Drones fleet at maximum capacity')
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
    service.delete_by_id(id, foreign_tables=[loads_service.model.table])
    return data_response({})


@handler.get('/<id:int>/medications')
def handle_loaded_medications(id):
    '''
    Retrieves the full list of medications loaded to the given drone id
    '''
    filters = MultiDict()
    filters.append('drone_id', f'{id}')
    loads = loads_service.get_all_records(filters)
    meds_list = []
    for load in loads:
        med = medications_service.get_record_by_id(load['medication_id'])
        med['load'] = load
        meds_list.append(med)
    return data_response(meds_list)


handler.HELP = '''
<div>
<ul>
    <li>
        <details>
            <summary>GET /drones</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X GET 'http://127.0.0.1:8080/api/v1/drones'
                </pre>
                <h4>Response</h4>
                <pre>
{
    "status": 200,
    "data": [
        {
            "drone_id": 1,
            "serial_number": "QWOIEJO1202115",
            "model": "Lightweight",
            "weight_limit": 250.0,
            "battery_capacity": 80,
            "state": "IDLE"
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
?state=[in]IDLE,LOADING&battery_capacity=[<=]25
                        </pre>
                    </div>
                </details>
            </div>
        </details>
    </li>
    
    <li>
        <details>
            <summary>POST /drones</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X POST 'http://127.0.0.1:8080/api/v1/drones/'
--header 'Authorization: Basic YWRtaW46YWRtaW4='
--header 'Content-Type: application/json'
--data-raw '{
    "serial_number": "LASKDWEOIR",
    "model": "Middleweight",
    "weight_limit": 10,
    "battery_capacity": 100,
    "state": "IDLE"
}'
                </pre>
                <h4>Response</h4>
                <pre>
HEADER Location: /api/v1/drones/10
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
            <summary>GET /drones/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X GET 'http://127.0.0.1:8080/api/v1/drones/1'
                </pre>
                <h4>Response</h4>
                <pre>
{
    "status": 200,
    "data": {
        "drone_id": 1,
        "serial_number": "QWOIEJO1202115",
        "model": "Lightweight",
        "weight_limit": 250.0,
        "battery_capacity": 80,
        "state": "IDLE"
    }
}
                </pre>
            </div>
        </details>
    </li>

    <li>
        <details>
            <summary>PUT /drones/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X PUT 'http://127.0.0.1:8080/api/v1/drones/1'
--header 'Authorization: Basic YWRtaW46YWRtaW4='
--header 'Content-Type: application/json'
--data-raw '{
    "serial_number": "LASKDWEOIR",
    "model": "Middleweight",
    "weight_limit": 10,
    "battery_capacity": 100,
    "state": "IDLE"
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
            <summary>DELETE /drones/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X DELETE 'http://127.0.0.1:8080/api/v1/drones/1'
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

    <li>
        <details>
            <summary>GET /drones/id:int/medications</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X GET 'http://127.0.0.1:8080/api/v1/drones/2/medications'
                </pre>
                <h4>Response</h4>
                <pre>
{
  "status": 200,
  "data": [
    {
      "medication_id": 1,
      "name": "Dalsy",
      "weight": 50.0,
      "code": "DALSY_1520",
      "image_id": 1,
      "load": {
        "load_id": 1,
        "drone_id": 2,
        "medication_id": 1,
        "quantity": 2
      }
    },
    ...
  ]
}
                </pre>
            </div>
        </details>
    </li>

</ul>
</div>
'''
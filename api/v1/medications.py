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
from db.models.load import model as load_model

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
    service.delete_by_id(id, foreign_tables=[load_model.table])
    return data_response({})


handler.HELP = '''
<div>
<ul>
    <li>
        <details>
            <summary>GET /medications</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X GET 'http://127.0.0.1:8080/api/v1/medications'
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
            "image_id": 1
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
?weight=[<]50
                        </pre>
                    </div>
                </details>
            </div>
        </details>
    </li>
    
    <li>
        <details>
            <summary>POST /medications</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X POST 'http://127.0.0.1:8080/api/v1/medications/'
--header 'Authorization: Basic YWRtaW46YWRtaW4='
--header 'Content-Type: application/json'
--data-raw '{
    "name": "Dipirone",
    "weight": 68,
    "code": "DIP_866TUY_458",
    "image_id": 1
}'
                </pre>
                <h4>Response</h4>
                <pre>
HEADER Location: /api/v1/medications/7
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
            <summary>GET /medications/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X GET 'http://127.0.0.1:8080/api/v1/medications/1'
                </pre>
                <h4>Response</h4>
                <pre>
{
    "status": 200,
    "data": {
        "medication_id": 1,
        "name": "Dalsy",
        "weight": 50.0,
        "code": "DALSY_1520",
        "image_id": 1
  }
}
                </pre>
            </div>
        </details>
    </li>

    <li>
        <details>
            <summary>PUT /medications/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X PUT 'http://127.0.0.1:8080/api/v1/medications/1'
--header 'Authorization: Basic YWRtaW46YWRtaW4='
--header 'Content-Type: application/json'
--data-raw '{
    "name": "Vicodin",
    "weight": 50,
    "code": "VC_4589789",
    "image_id": 1
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
            <summary>DELETE /medications/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X DELETE 'http://127.0.0.1:8080/api/v1/medications/1'
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
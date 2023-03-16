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
from api.services import images_service as service
from auth.basic import check_credentials
from db.models.medication import model as medication_model

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
    return data_response(service.get_all_records())


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
    service.delete_by_id(id, foreign_tables=[medication_model.table])
    return data_response({})


handler.HELP = '''
<div>
<ul>
    <li>
        <details>
            <summary>GET /images</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X GET 'http://127.0.0.1:8080/api/v1/images'
                </pre>
                <h4>Response</h4>
                <pre>
{
    "status": 200,
    "data": [
        {
            "image_id": 1,
            "mime": "image/jpeg",
            "base64": "/9j/4AAQSkZJRgABAQAAAQABAA...ACAEAIAQAgP//Z"
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
?mime=image/jpeg
                        </pre>
                    </div>
                </details>
            </div>
        </details>
    </li>
    
    <li>
        <details>
            <summary>POST /images</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X POST 'http://127.0.0.1:8080/api/v1/images/'
--header 'Authorization: Basic YWRtaW46YWRtaW4='
--header 'Content-Type: application/json'
--data-raw '{
    "mime": "image/png",
    "base64": "/9j/4AAQSkZJRgABAQAAAQABAA...ACAEAIAQAgP//Z"
}'
                </pre>
                <h4>Response</h4>
                <pre>
HEADER Location: /api/v1/images/7
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
            <summary>GET /images/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X GET 'http://127.0.0.1:8080/api/v1/images/1'
                </pre>
                <h4>Response</h4>
                <pre>
{
    "status": 200,
    "data": {
        "image_id": 1,
        "mime": "image/jpeg",
        "base64": "/9j/4AAQSkZJRgABAQAAAQABAA...ACAEAIAQAgP//Z"
  }
}
                </pre>
            </div>
        </details>
    </li>

    <li>
        <details>
            <summary>PUT /images/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X PUT 'http://127.0.0.1:8080/api/v1/images/1'
--header 'Authorization: Basic YWRtaW46YWRtaW4='
--header 'Content-Type: application/json'
--data-raw '{
    "mime": "image/png",
    "base64": "/9j/4AAQSkZJRgABAQAAAQABAA...ACAEAIAQAgP//Z"
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
            <summary>DELETE /images/id:int</summary>
            <div>
                <h4>Request</h4>
                <pre>
curl -X DELETE 'http://127.0.0.1:8080/api/v1/images/1'
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
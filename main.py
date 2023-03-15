from http import HTTPStatus
from bottle import response
from api.api_bottle import ApiBottle
import api.v1
from db.sqlite import SqliteHelper as helper
from db.setup import run_migrations
import audit_task

run_migrations(helper.get_instance())
audit_task.run()
root = application = ApiBottle()

@root.hook('after_request')
def enable_cors():
    '''
    Add headers to enable CORS
    '''
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

@root.hook('after_request')
def set_cache_control_policy():
    '''
    Set a default cache control policy
    '''
    response.headers['Cache-Control'] = 'no-store'

@root.route('/', method = 'OPTIONS')
@root.route('/<path:path>', method = 'OPTIONS')
def options_handler(path = None):
    return

# delegate to actual API endpoint handler
root.mount('/api/v1', api.v1.handler)

@root.get('/')
def index():
    '''
    A default response for the root path.
    '''
    return '''<h1>Welcome to Dronery REST API</h1>
    <h2>Available endpoints:</h2>
    <ul>
        <li><a href="api/v1">API v1</a></li>
    </ul>
    '''

if __name__ == '__main__':
    # if Gunicorn is installed (using Bottle's adapter)
    # bottle.run(server='gunicorn', host = '127.0.0.1', port = 8000)
    
    # if uWSGI is installed (no Bottle's adapter available, so it is called from CLI)
    # $ uwsgi --http :8000 --wsgi-file main.py
    
    # For development (uses Python’s built-in WSGI reference server)
    root.run()
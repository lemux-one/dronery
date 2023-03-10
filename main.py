from http import HTTPStatus
from bottle import (
    Bottle,
    response
)
from api.v1.handler import handler as api_v1
from api.utils import error_response
from db.sqlite import helper
from db.setup import run_migrations

run_migrations(helper)

root = application = Bottle()

@root.route('/')
def index():
    return 'Welcome to Dronery REST API'

# delegate to actual API endpoint handler
root.mount('/api/v1', api_v1)

@root.route('/<endpoint:path>')
def unknown(endpoint):
    '''
    Handle every path not already mapped to a valid API call as 404 error.
    '''
    return error_response(f'Unknown endpoint: {endpoint}', HTTPStatus.NOT_FOUND)


if __name__ == '__main__':
    # if Gunicorn is installed (using Bottle's adapter)
    # bottle.run(server='gunicorn', host = '127.0.0.1', port = 8000)
    
    # if uWSGI is installed (no Bottle's adapter available, so it is called from CLI)
    # $ uwsgi --http :8000 --wsgi-file main.py
    
    # For development (uses Python’s built-in WSGI reference server)
    root.run()
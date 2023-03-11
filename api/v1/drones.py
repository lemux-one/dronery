from bottle import Bottle
from http import HTTPStatus
from api.utils import (
    data_response,
    error_response,
    error_404
)
from db.sqlite import helper

drones_handler = Bottle()

'''
A Drone has:
 - serial number (100 characters max);
 - model (Lightweight, Middleweight, Cruiserweight, Heavyweight);
 - weight limit (500gr max);
 - battery capacity (percentage);
 - state (IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING)
'''

@drones_handler.get('/')
def list():
    '''
    Lists available drones
    '''
    ok, drones = helper.query('select * from drones;')
    if ok:
        return data_response(drones)
    else:
        return error_response()


@drones_handler.get('/<id:int>')
def show(id):
    '''
    Shows details for the given drone ID.
    '''
    ok, drones = helper.query('select * from drones where id = ?', (id,))
    if ok and drones:
        return data_response(drones[0])
    else:
        return error_404(f'Drone with id {id} was not found')


@drones_handler.route('/<endpoint:path>')
def unknown(endpoint):
    '''
    Captures any invalid/unknown path and responds with a custom 404 notice.
    '''
    return error_404(f'Unknown endpoint "{endpoint}"')
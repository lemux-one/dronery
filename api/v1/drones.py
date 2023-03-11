from http import HTTPStatus
from bottle import abort
from api.api_bottle import ApiBottle
from api.utils import (
    data_response,
    error_response
)
from db.sqlite import helper

drones_handler = ApiBottle()

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
        abort(HTTPStatus.NOT_FOUND, f'Drone with id "{id}" was not found')
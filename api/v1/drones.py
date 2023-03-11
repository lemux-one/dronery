from bottle import Bottle
from api.utils import (
    data_response,
    error_response
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
    ok, drones = helper.query('select * from "drones";')
    if ok:
        return data_response(drones)
    else:
        return error_response()
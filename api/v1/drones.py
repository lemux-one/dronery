from bottle import Bottle
from api.utils import json_response

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
    drones = [
        {
            'serial_number': 'LW001',
            'model': 'Lightweight',
            'weight_limit': 150,
            'battery_capacity': 85,
            'state': 'IDLE'
        }
    ]
    return json_response(drones)
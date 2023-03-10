from bottle import Bottle
from .drones import drones_handler

handler = Bottle()
handler.mount('/drones', drones_handler)
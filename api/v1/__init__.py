from api.api_bottle import ApiBottle
from .drones import drones_handler

handler = ApiBottle()
handler.mount('/drones', drones_handler)
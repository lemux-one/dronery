from api.api_bottle import ApiBottle
from .drones import handler as drones_handler

handler = ApiBottle()
handler.mount('/drones', drones_handler)
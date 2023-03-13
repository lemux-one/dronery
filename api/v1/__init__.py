from api.api_bottle import ApiBottle
from .drones import handler as drones_handler
from .medications import handler as medications_handler

handler = ApiBottle()
handler.mount('/drones', drones_handler)
handler.mount('/medications', medications_handler)
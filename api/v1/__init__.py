from api.api_bottle import ApiBottle
from .drones import handler as drones_handler
from .medications import handler as medications_handler
from .images import handler as images_handler

handler = ApiBottle()
handler.mount('/drones', drones_handler)
handler.mount('/medications', medications_handler)
handler.mount('/images', images_handler)
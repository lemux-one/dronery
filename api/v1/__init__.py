from api.api_bottle import ApiBottle
from .drones import handler as drones_handler
from .medications import handler as medications_handler
from .images import handler as images_handler
from .loads import handler as loads_handler

handler = ApiBottle()
handler.mount('/drones', drones_handler)
handler.mount('/medications', medications_handler)
handler.mount('/images', images_handler)
handler.mount('/loads', loads_handler)

@handler.get('/')
def handle_root():
    return '''<h1>API v1:</h1>
    <h2>Available endpoints:</h2>
    <ul>
        <li><a href="drones">Drones</a></li>
        <li><a href="medications">Medications</a></li>
        <li><a href="images">Images</a></li>
        <li><a href="loads">Loads</a></li>
    </ul>
    '''
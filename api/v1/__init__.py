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
    return f'''<h1>API v1:</h1>
    <h2>Available endpoints:</h2>
    <ul>
        <li>
            <details>
            <summary>Drones</summary>
            {drones_handler.HELP}
            </details>
        </li>
        <li>
            <details>
            <summary>Medications</summary>
            {medications_handler.HELP}
            </details>
        </li>
        <li>
            <details>
            <summary>Images</summary>
            {images_handler.HELP}
            </details>
        </li>
        <li>
            <details>
            <summary>Loads</summary>
            {loads_handler.HELP}
            </details>
        </li>
    </ul>
    '''
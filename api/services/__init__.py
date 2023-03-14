from db.sqlite import helper
from db.service import Service

from db.models import (
    drone,
    image,
    medication,
    load
)

drones_service = Service(dbhelper=helper, model=drone.model)
images_service = Service(dbhelper=helper, model=image.model)
medications_service = Service(dbhelper=helper, model=medication.model)
loads_service = Service(dbhelper=helper, model=load.model)
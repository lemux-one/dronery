from db.model import Model, Field

'''
A Drone has:
- serial number (100 characters max);
- model (Lightweight, Middleweight, Cruiserweight, Heavyweight);
- weight limit (500gr max);
- battery capacity (percentage);
- state (IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING)
'''
model = Model(table='drones')
model.add_field(Field(name='drone_id', dtype=Field.INTEGER_TYPE, pk=True))
model.add_field(Field(name='serial_number', dtype=Field.VARCHAR_TYPE, 
    max=100, unique=True))
model.add_field(Field(name='model', dtype=Field.SELECT_TYPE, 
    options=['Lightweight', 'Middleweight', 'Cruiserweight', 'Heavyweight']))
model.add_field(Field(name='weight_limit', dtype=Field.DOUBLE_TYPE, 
    min=0, max=500))
model.add_field(Field(name='battery_capacity', dtype=Field.INTEGER_TYPE, 
    min=0, max=100))
model.add_field(Field(name='state', dtype=Field.SELECT_TYPE, 
    options=['IDLE', 'LOADING', 'LOADED', 'DELIVERING', 'DELIVERED', 'RETURNING']))
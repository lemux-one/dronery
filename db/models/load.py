from db.model import Model, Field

'''
A Load has:
- drone_id (FK);
- medication_id (FK).
- quantity (how many units of the medication);
'''
model = Model(table='loads')
model.add_field(Field(name='load_id', dtype=Field.INTEGER_TYPE, pk=True))
model.add_field(Field(name='drone_id', dtype=Field.INTEGER_TYPE, 
    fk=True, ftable='drones'))
model.add_field(Field(name='medication_id', dtype=Field.INTEGER_TYPE, 
    fk=True, ftable='medications'))
model.add_field(Field(name='quantity', dtype=Field.INTEGER_TYPE, min=0))

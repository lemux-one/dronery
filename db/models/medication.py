from db.model import Model, Field

'''
A Medication has:
- name (allowed only letters, numbers, '-', '_');
- weight;
- code (allowed only upper case letters, underscore and numbers);
- image (picture of the medication case).
'''
model = Model(table='medications')
model.add_field(Field(name='medication_id', dtype=Field.INTEGER_TYPE, pk=True))
model.add_field(Field(name='name', dtype=Field.VARCHAR_TYPE, unique=True,
    max=100, regex=r'^([a-z]|[A-Z]|\d|-|_)+$'))
model.add_field(Field(name='weight', dtype=Field.DOUBLE_TYPE, min=0))
model.add_field(Field(name='code', dtype=Field.VARCHAR_TYPE, unique=True,
    max=100, regex=r'^([A-Z]|\d|_)+$'))
model.add_field(Field(name='image_id', dtype=Field.INTEGER_TYPE, 
    fk=True, ftable='images'))
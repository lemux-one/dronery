from db.model import Model, Field

'''
An image has:
- base64 (Base64 encoded representation of the binary file);
- mime (MIME string to know what type of image it is: image/jpeg, image/png, etc)
'''
model = Model(table='images')
model.add_field(Field(name='image_id', dtype=Field.INTEGER_TYPE, pk=True))
model.add_field(Field(name='mime', dtype=Field.VARCHAR_TYPE, regex=r'^image/(png|jpeg)$'))
model.add_field(Field(name='base64', dtype=Field.VARCHAR_TYPE, min=1))
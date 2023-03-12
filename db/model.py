from db import validator

class Field:
    
    INTEGER_TYPE = 'integer'
    VARCHAR_TYPE = 'varchar'
    SELECT_TYPE = 'select'

    def __init__(self, name: str, dtype: str, min: float = None, max: float = None, options: list = None,
            unique: bool = False, null: bool = False, validator = None, pk: bool = False):
        self.name = name
        self.dtype = dtype
        self.max = max
        self.min = min
        self.options = options if options else []
        self.unique = unique
        self.null = null
        self.validator = validator
        self.pk = pk

class Model:
    def __init__(self, table: str):
        self.table = table
        self.fields = []
        self.fields_map = {}
        self.pk = None
        self.obj = {}
    
    def add_field(self, field: Field) -> None:
        self.fields.append(field)
        self.fields_map[field.name] = field
        if field.pk:
            self.pk = field
    
    def from_dict(self, source: dict, include_pk: bool = False) -> None:
        skeys = source.keys()
        for field in self.fields:
            if not field.pk or include_pk:
                if field.name in skeys:
                    ok, hint = self.validate(field.name, source[field.name])
                    if ok:
                        self.obj[field.name] = source[field.name]
                    else:
                        self.obj.clear()
                        raise ValueError(f'Invalid "{field.name}": {hint}')
                else:
                    self.obj.clear()
                    raise ValueError(f'Required field "{field.name}" not found in given data')
    
    def validate(self, field_name: str, value) -> (bool, str):
        field = self.fields_map.get(field_name)
        if not field:
            return False
        if callable(field.validator):
            return field.validator(value)
        else:
            dtype = field.dtype.lower()
            if dtype == Field.INTEGER_TYPE:
                return validator.validate_int(value, field.min, field.max)
            elif dtype == Field.VARCHAR_TYPE:
                return validator.validate_varchar(value, field.min, field.max)
            elif dtype == Field.SELECT_TYPE:
                return validator.validate_select(value, field.options)
            else:
                raise ValueError(f'Unable to find a validator for field: {field.name}')
        

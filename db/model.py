from db import validator

class Field:
    
    INTEGER_TYPE = 'integer'
    VARCHAR_TYPE = 'varchar'
    SELECT_TYPE = 'select'

    def __init__(self, name: str, dtype: str, min: float = None, max: float = None, 
            options: list = None, unique: bool = False, null: bool = False, regex: str = None,
            validator = None, pk: bool = False, fk: bool = False, ftable: str = None):
        self.name = name
        self.dtype = dtype
        self.max = max
        self.min = min
        self.options = options if options else []
        self.unique = unique
        self.null = null
        self.regex = regex
        self.validator = validator
        self.pk = pk
        self.fk = fk
        self.ftable = ftable

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
                    ok, hint = self.validate(field, source[field.name])
                    if ok:
                        self.obj[field.name] = source[field.name]
                    else:
                        self.obj.clear()
                        raise ValueError(f'Invalid "{field.name}": {hint}')
                else:
                    self.obj.clear()
                    raise ValueError(f'Required field "{field.name}" not found in given data')
    
    def validate(self, field: Field, value) -> (bool, str):
        if not field:
            return False
        if callable(field.validator):
            return field.validator(field, value)
        else:
            dtype = field.dtype.lower()
            if dtype == Field.INTEGER_TYPE:
                return validator.validate_int(field, value)
            elif dtype == Field.VARCHAR_TYPE:
                return validator.validate_varchar(field, value)
            elif dtype == Field.SELECT_TYPE:
                return validator.validate_select(field, value)
            else:
                raise ValueError(f'Unable to find a validator for field: {field.name}')
        

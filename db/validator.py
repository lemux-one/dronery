import re

#
#   Common validators
#
def validate_int(field, value) -> (bool, str):
    if type(value) != int:
        return False, 'Integer only'
    if field.min and value < field.min:
        return False, f'Minimum of {field.min}'
    if field.max and value > field.max:
        return False, f'Maximum of {field.max}'
    return True, ''

def validate_varchar(field, value) -> (bool, str):
    if type(value) != str:
        return False, 'String only'
    if field.min and len(value) < int(field.min):
        return False, f'At least {int(field.min)} characters'
    if field.max and len(value) > int(field.max):
        return False, f'Up to {int(field.max)} characters'
    if field.regex and not re.match(field.regex, value):
        return False, f'Must match pattern "{field.regex}"'
    return True, ''

def validate_select(field, value) -> (bool, str):
    if not field.options:
        return False, 'No options to select from'
    if type(value) != type(field.options[0]):
        return False, 'Type mismatch'
    if value in field.options:
        return True, ''
    else:
        return False, f'One of {field.options} only'


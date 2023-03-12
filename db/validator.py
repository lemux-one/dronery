#
#   Common validators
#
def validate_int(value, min: float = None, max: float = None) -> (bool, str):
    if not isinstance(value, int):
        return False, 'Integer only'
    if min and value < min:
        return False, f'Minimum of {min}'
    if max and value > max:
        return False, f'Maximum of {max}'
    return True, ''

def validate_varchar(value, min: float = None, max: float = None) -> (bool, str):
    if not isinstance(value, str):
        return False, 'String only'
    if min and len(value) < int(min):
        return False, f'At least {int(min)} characters'
    if max and len(value) > int(max):
        return False, f'Up to {int(max)} characters'
    return True, ''

def validate_select(value, options: list) -> (bool, str):
    if not options:
        return False, 'No options to select from'
    if type(value) != type(options[0]):
        return False, 'Type mismatch'
    if value in options:
        return True, ''
    else:
        return False, f'One of {options} only'


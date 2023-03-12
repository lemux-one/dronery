import unittest
from db import validator
from db.model import Field

class TestValidators(unittest.TestCase):

    def test_int_validator(self):
        field = Field('test', Field.INTEGER_TYPE)
        correct = 548
        self.assertTrue(validator.validate_int(field, correct)[0])
        wrong = 'asd'
        self.assertFalse(validator.validate_int(field, wrong)[0])
    
    def test_varchar_validator(self):
        field = Field('test', Field.VARCHAR_TYPE)
        correct = 'some string'
        field.max = 11
        self.assertTrue(validator.validate_varchar(field, correct)[0])
        field.max = 5
        self.assertFalse(validator.validate_varchar(field, correct)[0])
        field.min = 50
        self.assertFalse(validator.validate_varchar(field, correct)[0])
        wrong = 468
        self.assertFalse(validator.validate_varchar(field, wrong)[0])
    
    def test_select_validator(self):
        field = Field('test', Field.SELECT_TYPE, options=['one', 'two'])
        self.assertTrue(validator.validate_select(field, 'one')[0])
        self.assertTrue(validator.validate_select(field, 'two')[0])
        self.assertFalse(validator.validate_select(field, 'five')[0])
        self.assertFalse(validator.validate_select(field, 5)[0])
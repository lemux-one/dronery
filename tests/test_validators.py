import unittest
from db import validator

class TestValidators(unittest.TestCase):

    def test_int_validator(self):
        correct = 548
        self.assertTrue(validator.validate_int(correct)[0])
        wrong = 'asd'
        self.assertFalse(validator.validate_int(wrong)[0])
    
    def test_varchar_validator(self):
        correct = 'some string'
        self.assertTrue(validator.validate_varchar(correct, max=11)[0])
        self.assertFalse(validator.validate_varchar(correct, max=5)[0])
        self.assertFalse(validator.validate_varchar(correct, min=50)[0])
        wrong = 468
        self.assertFalse(validator.validate_varchar(wrong)[0])
    
    def test_select_validator(self):
        options = ['one', 'two']
        self.assertTrue(validator.validate_select('one', options)[0])
        self.assertTrue(validator.validate_select('two', options)[0])
        self.assertFalse(validator.validate_select('five', options)[0])
        self.assertFalse(validator.validate_select(5, options)[0])
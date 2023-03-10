import unittest
import json
from http import HTTPStatus
from api.utils import (
    json_response,
    error_response
)

class TestUtils(unittest.TestCase):
    
    def test_json_response(self):
        payload = {
            'key': 'value'
        }
        json_str = json_response(payload)
        self.assertTrue(isinstance(json_str, str))
        self.assertEqual(json_str, '{"key": "value"}')


    def test_error_response(self):
        reason = 'something happend'
        json_str = error_response(reason, HTTPStatus.NOT_FOUND)
        self.assertTrue(isinstance(json_str, str))
        json_dict = json.loads(json_str)
        self.assertEqual(json_dict['reason'], reason)
        self.assertEqual(json_dict['status'], 404)
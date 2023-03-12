import unittest
import json
from http import HTTPStatus
from api.utils import (
    json_response,
    error_response,
    data_response
)

class TestUtils(unittest.TestCase):
    
    def test_json_response(self):
        payload = {
            'key': 'value'
        }
        json_str = json_response(payload, HTTPStatus.OK)
        self.assertTrue(isinstance(json_str, str))
        self.assertEqual(json_str, '{"key": "value"}')


    def test_data_response(self):
        data = {
            'key': 'value'
        }
        payload_raw = data_response(data)
        self.assertTrue(isinstance(payload_raw, str))
        payload = json.loads(payload_raw)
        self.assertTrue('status' in payload.keys())
        self.assertTrue('data' in payload.keys())
        self.assertEqual(payload['data']['key'], data['key'])


    def test_error_response(self):
        reason = 'something happend'
        resp = error_response(reason, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertTrue(isinstance(resp, str))
        json_dict = json.loads(resp)
        self.assertEqual(json_dict['reason'], reason)
        self.assertEqual(json_dict['status'], 500)

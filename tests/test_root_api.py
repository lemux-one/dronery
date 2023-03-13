import unittest
import requests as req
from http import HTTPStatus
import json

class TestRootApi(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8080'
    

    def test_index_endpoint(self):
        try:
            resp = req.get(self.base_url + '/')
        except Exception:
            self.fail('API server not running')
        else:
            self.assertEqual(resp.status_code, HTTPStatus.OK)
            self.assertNotEqual(resp.headers['Content-Type'], 'application/json')
    

    def test_unknow_endpoint(self):
        try:
            resp = req.get(self.base_url + '/unknown/endpoint')
        except Exception:
            self.fail('API server not running')
        else:
            self.assertNotEqual(resp.status_code, HTTPStatus.OK)
            self.assertEqual(resp.headers['Content-Type'], 'application/json')
            payload = json.loads(resp.content)
            self.assertTrue('status' in payload.keys())
            self.assertTrue('reason' in payload.keys())
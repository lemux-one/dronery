import unittest
import requests as req
from http import HTTPStatus
import json

class TestRootApi(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8080'
    

    def test_index_endpoint(self):
        resp = req.get(self.base_url + '/')
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertNotEqual(resp.headers['Content-Type'], 'application/json')
    

    def test_unknow_endpoint(self):
        resp = req.get(self.base_url + '/unknown/endpoint')
        self.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(resp.headers['Content-Type'], 'application/json')
        
        payload = json.loads(resp.content)
        self.assertTrue('status' in payload.keys())
        self.assertTrue('reason' in payload.keys())
        self.assertTrue(payload['reason'].find('Unknown endpoint:') >= 0)
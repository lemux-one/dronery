import unittest
import requests as req
from http import HTTPStatus
import json

class TestDronesHandler(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8080'


    def test_drones_listing(self):
        resp = req.get(self.base_url + '/api/v1/drones')
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.headers['Content-Type'], 'application/json')

        payload = json.loads(resp.content)
        self.assertTrue(isinstance(payload, dict))
        self.assertTrue('status' in payload.keys())
        self.assertEqual(payload['status'], HTTPStatus.OK)

        self.assertTrue('data' in payload.keys())
        drones_list = payload['data']

        if len(drones_list) > 0:
            drone = drones_list[0]
            self.assertTrue('serial_number' in drone.keys())
            self.assertTrue('model' in drone.keys())
            self.assertTrue('weight' in drone.keys())
            self.assertTrue('battery_capacity' in drone.keys())
            self.assertTrue('state' in drone.keys())

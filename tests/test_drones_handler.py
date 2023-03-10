import unittest
import requests as req
from http import HTTPStatus
import json

class TestDronesHandler(unittest.TestCase):
    def test_drones_listing(self):
        resp = req.get('http://127.0.0.1:8080/api/v1/drones')
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.headers['Content-Type'], 'application/json')

        drones_list = json.loads(resp.content)
        self.assertTrue(isinstance(drones_list, list))

        if len(drones_list) > 0:
            drone = drones_list[0]
            self.assertTrue('serial_number' in drone.keys())
            self.assertTrue('model' in drone.keys())
            self.assertTrue('weight_limit' in drone.keys())
            self.assertTrue('battery_capacity' in drone.keys())
            self.assertTrue('state' in drone.keys())

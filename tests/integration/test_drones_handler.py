import unittest
from http import HTTPStatus
import json
from boddle import boddle
import bottle
from settings import Config

class TestDronesHandler(unittest.TestCase):

    app = None
    base_path = '/api/v1/drones'

    def setUp(self):
        if self.app is None:
            Config.set('TESTING', True)
            Config.set('DB_NAME', ':memory:')
            from db.sqlite import SqliteHelper
            from db.setup import run_migrations
            run_migrations(SqliteHelper.get_instance())
            import api.v1.drones as drones_app
            self.app = drones_app

    def test_handle_list(self):
        with boddle(path=self.base_path):
            content = self.app.handle_list()
            resp = bottle.response
            self.assertIsNotNone(resp)
            self.assertEqual(resp.status_code, HTTPStatus.OK)
            self.assertEqual(resp.headers['Content-Type'], 'application/json')

            payload = json.loads(content)
            self.assertTrue(isinstance(payload, dict))
            self.assertTrue('status' in payload.keys())
            self.assertEqual(payload['status'], HTTPStatus.OK)

            self.assertTrue('data' in payload.keys())
            drones_list = payload['data']

            if len(drones_list) > 0:
                drone = drones_list[0]
                self.assertTrue('serial_number' in drone.keys())
                self.assertTrue('model' in drone.keys())
                self.assertTrue('weight_limit' in drone.keys())
                self.assertTrue('battery_capacity' in drone.keys())
                self.assertTrue('state' in drone.keys())

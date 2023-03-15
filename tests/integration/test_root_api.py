import unittest
from http import HTTPStatus
import json
from boddle import boddle
import bottle
from settings import Config

class TestRootApi(unittest.TestCase):
    
    app = None

    def setUp(self):
        if self.app is None:
            Config.set('TESTING', True)
            Config.set('DB_NAME', ':memory:')
            import main
            self.app = main


    def test_index(self):
        with boddle(path='/', method='GET'):
            content = self.app.index()
            resp = bottle.response
            self.assertEqual(resp.status_code, HTTPStatus.OK)
            self.assertTrue(content.find('Dronery REST API') > -1)
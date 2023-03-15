import unittest
from http import HTTPStatus
import json
from boddle import boddle
import bottle

class TestRootApi(unittest.TestCase):
    
    app = None

    def setUp(self):
        if self.app is None:
            bottle.DEBUG = True
            from db import sqlite
            sqlite.helper = sqlite.SqliteHelper(in_memory=True)
            import main
            self.app = main


    def test_index(self):
        with boddle(path='/', method='GET'):
            content = self.app.index()
            resp = bottle.response
            self.assertEqual(resp.status_code, HTTPStatus.OK)
            self.assertTrue(content.find('Dronery REST API') > -1)
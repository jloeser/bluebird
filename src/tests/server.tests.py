#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import os
import sys
sys.path.append('../')
import server
import config

import unittest
import json

class ServerTestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        server.app.config.from_object(config)
        self.app = server.app.test_client()

    def tearDown(self):
        pass

    def get_json_response(self, url):
        return json.loads(self.app.get(url).data.decode('utf-8'))

    def test_root_url(self):
        data = self.get_json_response(config.ROOT_URL)
        assert config.VERSION_STR in data.keys()

    def test_serviceroot_url(self):
        data = self.get_json_response(config.SERVICEROOT_URL)
        assert "Virtual Redfish RESTful Root Service" in data['Name']

if __name__ == '__main__':
    unittest.main()

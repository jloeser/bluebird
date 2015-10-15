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

    def get_json(self, response):
        """
        Return Dict from JSON body in response.
        """
        return json.loads(response.data.decode('utf-8'))

    def test_root_url(self):
        """
        Requesting Root URI ('/redfish') shall return the version
        with a link to the Service Root URI.
        """
        response = self.app.get(config.URL['ROOT'])
        assert response.status_code == 200

        data = self.get_json(response)
        assert "v" + str(config.PROTOCOL_VERSION) in data.keys()

    def test_serviceroot_redirect(self):
        """
        Service Root URI has a trailing slash (e.g. '/redfish/v1/').
        A requested URI without a trailing slash shall be redirected
        to the Service Root URI. '/redfish/v1'-> 302:'/redfish/v1/'
        """
        response = self.app.get(config.URL['SERVICEROOT'])
        assert response.status_code == 302

if __name__ == '__main__':
    unittest.main()

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


class SessionTestCase(unittest.TestCase):

    _url = config.URL['SESSIONS']

    def setUp(self):
        self.app = server.app.test_client()

    def login(self, username, password):
        json_data = json.dumps({
                "UserName": username,
                "Password": password
        })
        return self.app.post(self._url, headers={
                'Content-Type': 'application/json',
            }, data=json_data, follow_redirects=True
        )

    def test_create_new_session(self):
        """
        A Redfish session is created by an HTTP POST to the Sessions
        collection resource, including the following POST body:

        POST /redfish/v1/SessionService/Sessions HTTP/1.1
        Host: <host-path>
        Content-Type: application/json; charset=utf-8
        Content-Length: <computed-length>
        Accept: application/json
        OData-Version: 4.0
        {
                "UserName": "<username>",
                "Password": "<password>"
        }
        """
        response = self.login(config.USER, config.PASS + 'x')
        assert response.status_code == 400

        response = self.login(config.USER + 'x', config.PASS)
        assert response.status_code == 400

        response = self.login(config.USER, config.PASS)
        assert response.status_code == 201
        assert b"User Session" in response.data

    def test_show_session(self):
        """
        Only show user session if a valid X-Auth-Token is present,
        otherwise get a 401.
        """
        response = self.app.get(self._url)
        assert response.status_code == 401

        response = self.login(config.USER, config.PASS)
        xauth = response.headers.get('X-Auth-Token')
        response = self.app.get(
                self._url,
                headers={'X-Auth-Token': xauth}
        )
        assert b"Id" in response.data


    def test_delete_session(self):
        """
        To terminate a session, a DELETE request to the resource (identified
        by the link returned in the Location header when the session was
        created) must be performed.
        """
        response = self.login(config.USER, config.PASS)
        assert response.status_code == 201

        location = response.headers.get('Location')

        response = self.app.delete(location)
        assert response.status_code == 200


if __name__ == '__main__':
    server.app.config['TESTING'] = True
    server.app.config.from_object(config)
    unittest.main()

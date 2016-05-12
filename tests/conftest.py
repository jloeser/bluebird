#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import json

import mock
import pytest
from core import PASS
from core import USER

import bluebird.server
from bluebird.core import URL
from bluebird.server.sessions.models import Session
from bluebird.server.sessions.models import BluebirdAuthentication


class Environment:

    def __init__(self):
        self.server = bluebird.server.app
        self.server.testing = True
        self.server.config.from_object(bluebird.core)
        self.client = self.server.test_client()

    def set_authentication_result(self, result):
        if result is None:
            Session.__dict__['_Session__shared_state']\
                    ['_Session__authentication_instance'] = None
        else:
            mock_auth = mock.create_autospec(BluebirdAuthentication)
            mock_auth.authenticate.return_value = result
            Session.set_authentication_instance(mock_auth)


@pytest.fixture(scope='module')
def env():
    return Environment()


@pytest.fixture(scope='function')
def create_xauth_session(env):
    env.set_authentication_result(True)

    response = env.client.post(URL['SESSIONS'], headers={
            'Content-Type': 'application/json'
            }, data=json.dumps({'UserName': USER, 'Password': PASS}))

    session_id = json.loads(response.data.decode('utf-8'))['Id']
    xauth = response.headers['X-Auth-Token']
    location = response.headers['Location']
    return (USER, session_id, xauth, location)

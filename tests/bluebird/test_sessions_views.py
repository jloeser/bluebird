#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import json

import pytest
from core import MIMETYPE
from core import PASS
from core import USER
from core import get_basic_auth

from bluebird.core import URL

login = json.dumps({'UserName': USER, 'Password': PASS})

login_data = [
        ('abcdef', login, True,  400, b'MalformedJSON'),
        (MIMETYPE, 'xx',  True,  400, b'MalformedJSON'),
        (MIMETYPE, '{}',  True,  400, b'UnrecognizedRequestBody'),
        (MIMETYPE, login, False, 403, b'NoValidSession'),
        (MIMETYPE, login, True,  201, b'User Session'),
        (MIMETYPE, login, None,  500, b'NoAuthenticationModule')
        ]


@pytest.mark.parametrize('content,data,authenticated,status_code,text',
                         login_data)
def test_create_session(content, data, authenticated, status_code, text, env):
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
    env.set_authentication_result(authenticated)
    response = env.client.post(
            URL['SESSIONS'],
            headers={'Content-Type': content},
            data=data)
    assert response.status_code == status_code
    assert text in response.data


def test_show_session(create_xauth_session, env):
    """
    Show user session overview.

    GET /redfish/v1/SessionService/Sessions/<session_id>
    """
    name, session_id, xauth, location = create_xauth_session

    response = env.client.get(
            URL['SESSIONS'] + '/' + str(session_id),
            headers={'X-Auth-Token': xauth})
    assert response.status_code == 200
    assert USER.encode('utf-8') in response.data


def test_delete_session(create_xauth_session, env):
    """
    To terminate a session, a DELETE request to the resource (identified
    by the link returned in the Location header when the session was
    created) must be performed.

    DELETE /redfish/v1/SessionService/Sessions/<session_id>
    """
    name, session_id, xauth, location = create_xauth_session
    response = env.client.get(URL['SESSIONS'] + '/' + str(session_id), headers={
            'X-Auth-Token': xauth})
    assert response.status_code == 200
    assert USER.encode('utf-8') in response.data

    response = env.client.delete(location)
    assert response.status_code == 200

    response = env.client.get(URL['SESSIONS'] + '/' + str(session_id), headers={
            'X-Auth-Token': xauth})
    assert response.status_code == 401
    assert b'NoValidSession' in response.data

    response = env.client.delete(URL['SESSIONS'] + '/1234')
    assert response.status_code == 200


def test_basic_auth(env):
    """
    Service shall support "Basic Authentication" (RFC 2617, Section 2).
    Services shall not require a client to create a session when Basic
    Auth is used.
    """

    basic_auth = get_basic_auth(USER + 'x', PASS)
    env.set_authentication_result(False)
    response = env.client.get(
            URL['SESSIONS'],
            headers={'Authorization': bytes.decode(basic_auth)})
    assert response.status_code == 401

    basic_auth = get_basic_auth(USER, PASS)
    env.set_authentication_result(True)
    response = env.client.get(
            URL['SESSIONS'],
            headers={'Authorization': bytes.decode(basic_auth)})
    assert response.status_code == 200

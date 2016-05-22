#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import json
import mock
import libvirt
import pytest

from core import MIMETYPE
from core import PASS
from core import USER
from core import get_basic_auth

from bluebird.core import URL
from bluebird.modules.libvirt import models
from bluebird.modules.libvirt.views import module
from bluebird.server import app


def setup_function(function):
    app.register_blueprint(module)
    models.LibvirtMonitor('test:///default')


def test_show_vms(env):
    """
    Show list of virtual machines (libvirt test driver: 1 system):

    "Members": [
        {
            "@odata.id": "/redfish/v1/Systems/test",
            ...
        }
    ]
    """
    response = env.client.get(URL['SYSTEMS'])
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert b'Computer System Collection' in response.data
    assert data['Members@odata.count'] == 1
    assert data['Members'][0]['@odata.id'] == '/redfish/v1/Systems/test'


def test_show_vm(env):
    """
    Show virtual machine details.
    """
    response = env.client.get(URL['SYSTEMS'] + '/test')
    data = json.loads(response.data.decode('utf-8'))

    assert data['Name'] == 'test'
    assert data['PowerState'] == 'On'
    assert data['Description'] == 'Virtual machine'
    assert data['SystemType'] == 'Virtual'

    response = env.client.get(URL['SYSTEMS'] + '/NotAvailable')
    assert response.status_code == 404
    assert b'ResourceMissingAtURI' in response.data


class TestVMPowerCycle():

    __url = URL['SYSTEMS'] + '/test/Actions/ComputerSystem.Reset'
    __post = '{{"ResetType": "{}"}}'

    __reset_data = [
        ('On', 200, ''),
        ('Off', 200, '')
    ]

    def test_vm_powercycle_unauthorized(self, env):
        response = env.client.post(
                TestVMPowerCycle.__url,
                headers={'Content-Type': MIMETYPE},
                data=TestVMPowerCycle.__post.format('On')
                )
        assert response.status_code == 401
        assert b'NoValidSession' in response.data

        response = env.client.post(
                TestVMPowerCycle.__url,
                headers={'Content-Type': MIMETYPE, 'X-Auth-Token': '1234567'},
                data=TestVMPowerCycle.__post.format('On')
                )
        assert response.status_code == 401
        assert b'NoValidSession' in response.data

    @mock.patch('libvirt.openAuth')
    @pytest.mark.parametrize('cmd,status_code,msg', __reset_data)
    def test_vm_powercycle_basic_auth(self, mock_openauth, env, cmd,
                                      status_code, msg):

        mock_openauth.return_value = libvirt.open('test:///default')

        basic_auth = get_basic_auth(USER, PASS)
        env.set_authentication_result(True)
        response = env.client.post(
                TestVMPowerCycle.__url,
                headers={'Content-Type': MIMETYPE, 'Authorization': basic_auth},
                data=TestVMPowerCycle.__post.format('On')
        )

        assert response.status_code == status_code

    def test_vm_powercycle_session(self):
        pass

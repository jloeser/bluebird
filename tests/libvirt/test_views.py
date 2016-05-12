#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import json

from bluebird.core import URL
from bluebird.modules.libvirt import models
from bluebird.modules.libvirt.views import module
from bluebird.server import app


def setup_function(function):
    app.register_blueprint(module)
    models.LibvirtMonitor('test:///default')


def test_show_virtual_machines(env):
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


def test_show_virtual_machine(env):
    """
    Show virtual machine details.
    """
    response = env.client.get(URL['SYSTEMS'] + '/test')
    data = json.loads(response.data.decode('utf-8'))

    assert data['Name'] == 'test'
    assert data['PowerState'] == 'On'
    assert data['Description'] == 'Virtual machine'
    assert data['SystemType'] == 'Virtual'

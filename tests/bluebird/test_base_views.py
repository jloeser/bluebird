#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from bluebird.core import MAJOR_VERSION
from bluebird.core import REDFISH_MAJOR_VERSION
from bluebird.core import URL


def test_root_url(env):
    """
    Requesting Root URI ('/redfish') shall return the version
    with a link to the Service Root URI.
    """
    response = env.client.get(URL['ROOT'])
    assert response.status_code == 200
    assert REDFISH_MAJOR_VERSION.encode('utf-8') in response.data


def test_serviceroot_redirect(env):
    """
    Service Root URI has a trailing slash (e.g. '/redfish/v1/').
    A requested URI without a trailing slash shall be redirected
    to the Service Root URI. '/redfish/v1'-> 302:'/redfish/v1/'
    """
    response = env.client.get(URL['SERVICEROOT'])
    assert response.status_code == 302
    assert (response.headers['LOCATION'] ==
            'http://localhost/redfish/v{}/'.format(MAJOR_VERSION))


def test_serviceroot_url(env):
    """
    Requesting Service Root URI ('/redfish/v1/') shall return the
    ServiceRoot ressource.
    """
    response = env.client.get(URL['SERVICEROOT'] + '/')
    assert response.status_code == 200
    assert 'application/json' in response.headers['Content-Type']
    assert b'ServiceRoot' in response.data


def test_odata_url(env):
    """
    The URI ('/redfish/v1/odata') for the Redfish OData Service Document.
    """
    response = env.client.get(URL['SERVICEROOT'] + '/odata')
    assert response.status_code == 200
    assert 'application/json' in response.headers['Content-Type']


def test_metadata_url(env):
    """
    The URI ('/redfish/v1/$metadata') for the Redfish Metadata Document.
    """
    response = env.client.get(URL['SERVICEROOT'] + '/$metadata')
    assert response.status_code == 200
    assert 'application/xml' in response.headers['Content-Type']

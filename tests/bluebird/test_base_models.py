#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import mock

from bluebird.server.base import models


def test_server_instance():
    """
    Singleton shall return same object.
    """
    instance1 = models.Server()
    instance2 = models.Server()
    assert id(instance1) == id(instance2)


@mock.patch('bluebird.server.base.models.socket')
def test_server_hostname(mock_socket):
    """
    Server object shall return correct hostname and IP address. If not
    detectable, return 'N/A' (not available).
    """
    mock_socket.getfqdn.return_value = 'server.devel.example.org'
    mock_socket.gethostbyname.return_value = '192.168.1.10'

    server = models.Server()
    assert mock_socket.getfqdn.called
    assert server.get_fqdn() == 'server.devel.example.org'
    assert server.get_ip() == '192.168.1.10'

    server._Server__hostname = None
    assert server.get_fqdn() == 'N/A'
    assert server.get_ip() == 'N/A'

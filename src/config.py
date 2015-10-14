#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
PROGRAM_NAME = 'redfish-server'
PROGRAM_NAME_SHORT = 'rfserver'

LOGGER = {
        'NAME': PROGRAM_NAME_SHORT,
        'LEVEL': 'INFO'
}

SERVER = {
        'ADDRESS': '0.0.0.0',
        'PORT': 4443,
        'SSL_CRT': '../server.crt',
        'SSL_KEY': '../server.key',
        'DEBUG': True
}

MAJOR_VERSION = 0
MINOR_VERSION = 1
PROTOCOL_VERSION = 1

PROGRAM_VERSION = "{}.{}".format(MAJOR_VERSION, MINOR_VERSION)
VERSION_STR = "v" + str(PROTOCOL_VERSION)

USER = 'root'
PASS = 'test'

URL = {
        'ROOT': '/rest',
        'SERVICEROOT': '/rest/v{}'.format(PROTOCOL_VERSION)
}

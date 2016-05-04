#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from bluebird import log

PROGRAM_NAME = 'bluebird-server'
PROGRAM_NAME_SHORT = 'bluebird'

LOGGER = {
        'NAME': PROGRAM_NAME_SHORT,
        'LEVEL': 'INFO'
}

SERVER = {
        'ADDRESS': '0.0.0.0',
        'PORT': 4443,
        'SSL_CRT': '../server.crt',
        'SSL_KEY': '../server.key',
        'DEBUG': False
}

MAJOR_VERSION = 1
MINOR_VERSION = 0
ERRATA = 0

REDFISH_MAJOR_VERSION = 'v' + str(MAJOR_VERSION)
REDFISH_VERSION = '{}.{}.{}'.format(MAJOR_VERSION, MINOR_VERSION, ERRATA)

URL = {
        'ROOT': '/redfish',
        'SERVICEROOT': '/redfish/v{}'.format(MAJOR_VERSION),
        'SESSIONSERVICE': '/redfish/v{}/SessionService'.format(MAJOR_VERSION),
        'SESSIONS':
                '/redfish/v{}/SessionService/Sessions'.format(MAJOR_VERSION),
        'SYSTEMS': '/redfish/v{}/Systems'.format(MAJOR_VERSION)
}

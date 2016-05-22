#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
USER = 'tux'
PASS = 'pass'

MIMETYPE = 'application/json'


def get_basic_auth(username, password):
    import base64

    return b'Basic ' + base64.b64encode(
            bytes(username, 'utf-8') + b':' + bytes(password, 'utf-8')
    )

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2

# flake8: noqa

NAME = 'libvirt'

import os
TEMPLATES = os.path.dirname(__file__) + '/templates'

MONITOR_URI = 'qemu:///system'
MANAGE_URI  = 'qemu+libssh2://{username}@localhost:2222/system'

from .views import module
from .authentication import LocalUser
from bluebird.server.sessions.models import Session

Session.set_authentication_instance(LocalUser())


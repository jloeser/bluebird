#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2

# flake8: noqa

NAME = 'libvirt'

import os
TEMPLATES = os.path.dirname(__file__) + '/templates'

from rflibvirt.views import module

from bluebird.server.sessions.models import Session
from rflibvirt.authentication import LocalUser

Session.set_authentication_instance(LocalUser())


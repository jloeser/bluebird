#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
NAME = 'libvirt'

import os
TEMPLATES = os.path.dirname(__file__) + '/templates'

from rflibvirt.views import module

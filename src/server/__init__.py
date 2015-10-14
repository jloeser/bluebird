#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import os
import sys

from flask import Flask

app = Flask(__name__)

from server.base.views import module as baseModule
app.register_blueprint(baseModule)

from server.sessions.views import module as sessionModule
app.register_blueprint(sessionModule)

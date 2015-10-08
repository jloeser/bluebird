#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import config
from flask import Flask

app = Flask(__name__)

@app.route(config.ROOT)
def show_root():
    return "root"


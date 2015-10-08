#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from flask import Flask, url_for, Blueprint

app = Flask(__name__)

@app.route('/')
def show_root():
    return "root"


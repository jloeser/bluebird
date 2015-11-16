#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import os
import sys

from flask import Flask, request, abort, g

from rfserver.server.sessions.models import Session

app = Flask(__name__)

@app.before_request
def set_session_object():
    g.session = Session()

# only accept JSON on POST data
@app.before_request
def check_content_type():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            return
        else:
            abort(500)

# ...and we do only send JSON
@app.after_request
def set_content_type(response):
    response.headers['Content-Type'] = 'application/json'
    return response

from rfserver.server.base.views import module as baseModule
app.register_blueprint(baseModule)

from rfserver.server.sessions.views import module as sessionModule
app.register_blueprint(sessionModule)

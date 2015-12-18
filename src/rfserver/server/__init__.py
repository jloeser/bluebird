#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import os
import sys

from flask import Flask, request, abort, g

from rfserver.server.sessions.models import Session
from rfserver.server.helper.registry import error
import json

app = Flask(__name__,
        template_folder='{}/templates'.format(
                os.path.dirname(os.path.realpath(__file__))),
        static_folder='{}/static'.format(
                os.path.dirname(os.path.realpath(__file__))),
        )

@app.before_request
def set_session_object():
    """Set session object for current request"""
    g.session = Session()

@app.before_request
def check_content_type():
    """Check if incoming POST request is JSON"""
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            return
        else:
            return (error('Base', 'MalformedJSON'), 500)

@app.after_request
def set_content_type(response):
    """Always ship JSON, except for the metadata document"""
    if hasattr(g, 'metadata'):
        content = 'application/xml'
    else:
        content = 'application/json'

    response.headers['Content-Type'] = content
    return response

from rfserver.server.base.views import module as baseModule
app.register_blueprint(baseModule)

from rfserver.server.sessions.views import module as sessionModule
app.register_blueprint(sessionModule)

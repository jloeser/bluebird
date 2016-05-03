#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import os
import json

from flask import Flask
from flask import g
from flask import request

from bluebird.server.base.views import module as baseModule
from bluebird.server.helper.registry import error
from bluebird.server.sessions.models import Session
from bluebird.server.sessions.views import module as sessionModule

app = Flask(
        __name__,
        template_folder='{}/templates'.format(
                        os.path.dirname(os.path.realpath(__file__))
                ),
        static_folder='{}/static'.format(
                        os.path.dirname(os.path.realpath(__file__))
                ),
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
            try:
                json.loads(request.data.decode('utf-8'))
                return
            except (ValueError, TypeError, KeyError):
                pass

        return (error('Base', 'MalformedJSON'), 400)


@app.after_request
def set_content_type(response):
    """Always ship JSON, except for the metadata document"""
    if hasattr(g, 'metadata'):
        content = 'application/xml'
    else:
        content = 'application/json'

    response.headers['Content-Type'] = content
    return response

app.register_blueprint(baseModule)
app.register_blueprint(sessionModule)

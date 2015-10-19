#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from functools import wraps
from flask import g, flash, redirect, url_for, request, abort
from server.sessions.models import Session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.xauth = request.headers.get('X-Auth-Token')
        if g.xauth:
            result = g.session.check_xauth(g.xauth)
            if result:
                g.login = result
                return f(*args, **kwargs)

        g.basic_auth = request.headers.get('Authorization')
        if g.basic_auth:
            result = g.session.check_basic_auth(g.basic_auth)
            if result:
                g.login = None
                return f(*args, **kwargs)

        abort(401)
    return decorated_function

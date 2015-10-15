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
        if g.xauth is not None:
            result = g.session.check(g.xauth)
            if result:
                g.login = result
                return f(*args, **kwargs)
        abort(401)
    return decorated_function

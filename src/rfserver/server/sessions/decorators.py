#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from functools import wraps
from flask import g, redirect, url_for, request, abort
from rfserver.server.sessions.models import Session
from rfserver.server.helper.registry import error

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """X-Auth-Token and basic authentication decorator"""
        if xauth() or basic_authentication():
            return f(*args, **kwargs)
        else:
            return (error('Base', 'NoValidSession'), 401)
    return decorated_function

def xauth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """X-Auth-Token header decorator"""
        if xauth():
            return f(*args, **kwargs)
        else:
            return (error('Base', 'NoValidSession'), 401)
    return decorated_function

def basic_authentication_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Basic authentication decorator"""
        if basic_authentication():
            return f(*args, **kwargs)
        else:
            return (error('Base', 'NoValidSession'), 401)
    return decorated_function

def xauth():
    """Check for X-AUTH-TOKEN header"""
    g.xauth = request.headers.get('X-Auth-Token')
    if g.xauth:
        result = g.session.check_xauth(g.xauth)
        if result:
            g.login = result
            return True
    else:
        return False

def basic_authentication():
    """Check for basic authentication (RFC 2617, section 2)"""
    g.basic_auth = request.headers.get('Authorization')
    if g.basic_auth:
        result = g.session.check_basic_auth(g.basic_auth)
        if result:
            g.login = result
            return True
    else:
        return False


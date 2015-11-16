#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from rfserver.config import URL, PROTOCOL_VERSION
from rfserver.server.base.models import Server
from flask import Blueprint, render_template, redirect, g, current_app

module = Blueprint('base', __name__)

@module.before_request
def set_server_object():
    g.server = Server()

@module.route(URL['ROOT'])
def show_version():
    return render_template('base/version.json',
        version='v{}'.format(PROTOCOL_VERSION),
        url=URL['SERVICEROOT']
     )

@module.route(URL['SERVICEROOT'])
def redirect_serviceroot():
    return redirect(URL['SERVICEROOT'] + '/')

@module.route(URL['SERVICEROOT'] + '/')
def show_serviceroot():
    return render_template('base/serviceroot.json',
            module=current_app.config['MODULE'])

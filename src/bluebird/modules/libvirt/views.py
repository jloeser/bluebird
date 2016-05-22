#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import json

from flask import Blueprint
from flask import g
from flask import render_template
from flask import request

from bluebird.core import URL
from bluebird.server.base.models import Server
from bluebird.server.decorators import collection
from bluebird.server.helper.registry import error
from bluebird.server.sessions.decorators import login_required

from . import TEMPLATES
from .models import LibvirtManage
from .models import LibvirtMonitor

module = Blueprint('system', __name__, url_prefix=URL['SERVICEROOT'],
                   template_folder=TEMPLATES
                   )


@module.before_request
def set_libvirt_object():
    g.libvirt = LibvirtMonitor()


@module.route('/Systems', methods=['GET'])
@collection.odata_query_parameters_not_implemented
def list_domains():
    return render_template('ComputerSystemCollection.json', libvirt=g.libvirt)


@module.route('/Systems/<domain>', methods=['GET', 'POST'])
def show_domain(domain):
    domain = g.libvirt.get_domain(domain)
    if domain:
        return render_template('ComputerSystem.1.0.1.json', domain=domain,
                               server=Server()
                               )
    else:
        return (error('Base', 'ResourceMissingAtURI'), 404)


@module.route('/Systems/<domain>/Actions/ComputerSystem.Reset',
              methods=['POST']
              )
@login_required
def reset(domain):
    if not g.libvirt.get_domain(domain):
        return (error('Base', 'ResourceMissingAtURI'), 404)

    try:
        data = json.loads(request.data.decode('utf-8'))
        manager = LibvirtManage((g.login['USERNAME'], g.login['PASSWORD']))
        manager.reset(domain, data['ResetType'])
        return ('', 200)
    except Exception as e:
        return (str(e), 400)
        pass

    return ('', 400)

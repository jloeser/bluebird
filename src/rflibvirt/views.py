#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from bluebird.config import URL
from flask import Blueprint, jsonify, g, render_template, abort, request
from bluebird.server.base.models import Server
from bluebird.server.sessions.decorators import xauth_required, login_required
from rflibvirt.models import LibvirtMonitor, LibvirtManage
from rflibvirt import TEMPLATES
from bluebird.server.decorators import collection
from bluebird.server.helper.registry import error
import json

module = Blueprint('system', __name__, url_prefix=URL['SERVICEROOT'],
        template_folder=TEMPLATES)

@module.before_request
def set_libvirt_object():
    g.libvirt = LibvirtMonitor()
    # probe for domains which may have changed
    g.libvirt.probe()

@module.route('/Systems', methods=['GET'])
@collection.odata_query_parameters_not_implemented
def list_domains():
    return render_template('ComputerSystemCollection.json',
            libvirt=g.libvirt
    )

@module.route('/Systems/<domain>', methods=['GET', 'POST'])
def show_domains(domain):
    domain = g.libvirt.get_domain(domain)
    if domain:
        return render_template('ComputerSystem.1.0.1.json',
                domain=domain,
                server=Server()
        )
    else:
        return (error('Base', 'ResourceMissingAtURI'), 404)

@module.route('/Systems/<domain>/Actions/ComputerSystem.Reset',
        methods=['POST'])
@login_required
def reset(domain):
    dom = g.libvirt.get_domain(domain)

    if not dom:
        return (error('Base', 'ResourceMissingAtURI'), 404)

    try:
        data = json.loads(request.data.decode('utf-8'))
    except ValueError as e:
        return (error('Base', 'MalformedJSON'), 400)

    if 'ResetType' in data.keys():
        action = g.libvirt.valid_action(data['ResetType'])
        if action:
            credentials = (g.login['USERNAME'], g.login['PASSWORD'])
            execute = getattr(dom, action)
            credentials = (credentials)
            manager = LibvirtManage(credentials)
    return (error('Base', 'ActionNotSupported'), 500)

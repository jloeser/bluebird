#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from rfserver.config import URL
from flask import Blueprint, jsonify, g, render_template, abort, request
from rfserver.server.base.models import Server
from rfserver.server.sessions.decorators import xauth_required
from rflibvirt.models import Libvirt, RESET
from rflibvirt import TEMPLATES
from rfserver.server.decorators import collection
import json

module = Blueprint('system', __name__, url_prefix=URL['SERVICEROOT'],
        template_folder=TEMPLATES)

@module.before_request
def set_libvirt_object():
    g.libvirt = Libvirt()
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
        abort(404)

@module.route('/Systems/<domain>/Actions/ComputerSystem.Reset',
        methods=['POST'])
@xauth_required
def reset(domain):
    dom = g.libvirt.get_domain(domain)
    if dom:
        try:
            data = json.loads(request.data.decode('utf-8'))
        except ValueError as error:
            print(error)
            abort(500)

        if 'ResetType' in data.keys():
            username = g.login['USERNAME']
            action = data['ResetType']
            if action in RESET.keys():
                method = getattr(dom, RESET[action])
                method(username)
                pass
            return ("", 200)
        else:
            abort(500)
    else:
        abort(404)


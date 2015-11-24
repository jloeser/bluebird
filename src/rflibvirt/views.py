#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from rfserver.config import URL
from flask import Blueprint, jsonify, g, render_template, abort, request
from rfserver.server.base.models import Server
from rflibvirt.models import Libvirt, RESET
from rflibvirt import TEMPLATES
import json

module = Blueprint('system', __name__, url_prefix=URL['SERVICEROOT'],
        template_folder=TEMPLATES)

@module.before_request
def set_libvirt_object():
    g.libvirt = Libvirt()

@module.route('/Systems', methods=['GET'])
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
def reset(domain):
    dom = g.libvirt.get_domain(domain)
    if dom:
        try:
            data = json.loads(request.data.decode('utf-8'))
        except ValueError as error:
            print(error)
            abort(500)

        if 'ResetType' in data.keys():
            action = data['ResetType']
            if action in RESET.keys():
                method = getattr(dom, RESET[action])
                method()
                pass
            return ("", 200)
        else:
            abort(500)
    else:
        abort(404)


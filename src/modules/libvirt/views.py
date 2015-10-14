#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from config import URL
from flask import Blueprint, jsonify, g, render_template
from server.base.models import Server
from .models import Libvirt
from . import TEMPLATES

module = Blueprint('system', __name__, url_prefix=URL['SERVICEROOT'],
        template_folder=TEMPLATES)

@module.before_request
def set_libvirt_object():
    g.libvirt = Libvirt()

@module.after_request
def set_json_header(response):
    response.headers['Content-Type'] = 'application/json'
    return response

@module.route('/Systems')
def list_domains():
    return render_template('systems.json', libvirt=g.libvirt)

@module.route('/Systems/<domain>')
def show_domains(domain):
    domain = g.libvirt.get_domain(domain)
    return render_template('systems_domain.json',
            domain=domain,
            server=Server()
    )


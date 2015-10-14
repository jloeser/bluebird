#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from config import URL
from flask import Blueprint, jsonify, g
from .models import Libvirt

module = Blueprint('system', __name__, url_prefix=URL['SERVICEROOT'])

@module.before_request
def set_libvirt_object():
    g.libvirt = Libvirt()

@module.after_request
def set_json_header(response):
    response.headers['Content-Type'] = 'application/json'
    return response

@module.route('/Systems')
def list_domains():
    return jsonify(system='system')

@module.route('/Systems/<domain>')
def show_domains(domain):
    return jsonify(domain=domain)


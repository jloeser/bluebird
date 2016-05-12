#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from flask import Blueprint
from flask import current_app
from flask import g
from flask import redirect
from flask import render_template

from bluebird.core import REDFISH_MAJOR_VERSION
from bluebird.core import REDFISH_VERSION
from bluebird.core import URL
from bluebird.server.base.models import Server
from bluebird.server.sessions.decorators import login_required

module = Blueprint('base', __name__)


@module.before_request
def set_server_object():
    g.server = Server()


@module.route(URL['ROOT'], methods=['GET'])
def show_version():
    return render_template(
            'base/Version.json', version=REDFISH_MAJOR_VERSION,
            url=URL['SERVICEROOT'])


@module.route(URL['SERVICEROOT'], methods=['GET'])
def redirect_serviceroot():
    return redirect(URL['SERVICEROOT'] + '/')


@module.route(URL['SERVICEROOT'] + '/', methods=['GET'])
def show_serviceroot():
    return render_template(
            'base/ServiceRoot.1.0.0.json',
            redfish_version=REDFISH_VERSION)


@module.route(URL['SERVICEROOT'] + '/odata', methods=['GET'])
def show_odata_service_document():
    return current_app.send_static_file('odata')


@module.route(URL['SERVICEROOT'] + '/$metadata', methods=['GET'])
def show_redfish_metadata_document():
    g.metadata = True
    return current_app.send_static_file('$metadata')


@module.route(URL['SERVICEROOT'] + '/Registries', methods=['GET'])
@login_required
def show_registries():
    return current_app.send_static_file('Registries.json')


@module.route(URL['SERVICEROOT'] + '/Registries/Base', methods=['GET'])
@login_required
def show_base_registry():
    return current_app.send_static_file('Registries/Base.json')


@module.route(URL['SERVICEROOT'] + '/Registries/BluebirdServer',
              methods=['GET'])
@login_required
def show_redfishserver_registry():
    return current_app.send_static_file('Registries/BluebirdServer.json')


@module.route(URL['SERVICEROOT'] +
              '/RegistryStore/registries/en/Base.json', methods=['GET'])
@login_required
def show_base_registry_full():
    return current_app.send_static_file(
            'RegistryStore/registries/en/Base.json')


@module.route(URL['SERVICEROOT'] +
              '/RegistryStore/registries/en/BluebirdServer.json',
              methods=['GET'])
@login_required
def show_redfishserver_registry_full():
    return current_app.send_static_file(
            'RegistryStore/registries/en/BluebirdServer.json')

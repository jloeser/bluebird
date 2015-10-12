#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from flask import Flask, url_for, Blueprint, render_template, jsonify,\
        redirect, make_response, g, current_app
import socket

server = Blueprint('server', __name__, template_folder='templates')

class Server():

    _instance = None
    hostname = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Server, cls).__new__(
                    cls, *args, **kwargs
            )
        return cls._instance

    def __init__(self):
        self.hostname = socket.getfqdn()


@server.before_request
def set_server_object():
    g.server = Server()

@server.after_request
def set_json_header(response):
    response.headers['Content-Type'] = 'application/json'
    return response

@server.route('/rest')
def show_version():
    response = make_response(render_template('version.json',
        version=current_app.config['VERSION_STR'],
        url=current_app.config['SERVICEROOT_URL']
        ))
    return response

@server.route('/rest/v1')
def redirect_serviceroot():
    return redirect(current_app.config['SERVICEROOT_URL'])

@server.route('/rest/v1/')
def show_serviceroot():
    response = make_response(render_template('serviceroot.json',
            server=g.server
    ))
    return response


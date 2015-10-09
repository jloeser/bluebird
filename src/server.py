#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from flask import Flask, url_for, Blueprint, render_template, jsonify,\
        redirect, make_response, g
import socket

app = Flask(__name__)

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


@app.before_request
def before_request():
    g.server = Server()

@app.route('/rest')
def show_version():
    response = make_response(render_template('version.json',
        version=app.config['VERSION_STR'],
        url=app.config['SERVICEROOT_URL']
        ))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/rest/v1')
def redirect_serviceroot():
    return redirect(app.config['SERVICEROOT_URL'])

@app.route('/rest/v1/')
def show_serviceroot():
    response = make_response(render_template('serviceroot.json',
            server=g.server
    ))
    response.headers['Content-Type'] = 'application/json'
    return response


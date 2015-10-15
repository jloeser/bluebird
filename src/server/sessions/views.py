#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from flask import Blueprint, jsonify, g
from config import URL
from server.sessions.decorators import login_required

module = Blueprint('sessions', __name__, url_prefix=URL['SERVICEROOT'])

@module.route('/Sessions', methods=['POST'])
def create_session():
    print(g.xauth)
    return jsonify(session='session')

@module.route('/Sessions/<id>', methods=['DELETE'])
def delete_session(id):
    return jsonify(message='deleted')

@module.route('/Sessions/secret')
@login_required
def secret():
    return jsonify(message='secret')


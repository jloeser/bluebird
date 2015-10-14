#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from flask import Blueprint, jsonify
from config import URL

module = Blueprint('sessions', __name__, url_prefix=URL['SERVICEROOT'])

@module.route('/Sessions')
def show_session():
    return jsonify(session='session')


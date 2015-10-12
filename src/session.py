#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from flask import Flask, Blueprint

session = Blueprint('session', __name__, template_folder='templates',
        url_prefix='/rest/v1')

@session.route('/Sessions')
def list_system():
    return "sessions"



#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from flask import Flask, Blueprint
NAME = 'libvirt'

libvirt = Blueprint(NAME, __name__, template_folder='templates')

@libvirt.route('/system')
def list_system():
    return "system"

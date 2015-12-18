#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from rfserver.config import USER, PASS

class User():

    def is_authenticated(username, password):
        if username == USER and password == PASS:
            return True

        return False

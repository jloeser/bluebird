#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import socket

class Server():

    _instance = None
    _hostname = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Server, cls).__new__(
                    cls, *args, **kwargs
            )
        return cls._instance

    def __init__(self):
        self._hostname = socket.getfqdn()

    def getfqdn(self):
        return self._hostname

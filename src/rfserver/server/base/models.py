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
        Server._hostname = socket.getfqdn()
        return cls._instance

    def get_fqdn(self):
        return self._hostname

    def get_ip(self):
        try:
            ip = socket.gethostbyname(self._hostname)
            return ip
        except socket.gaierror:
            return ''

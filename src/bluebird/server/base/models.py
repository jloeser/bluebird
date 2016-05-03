#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import socket


class Server():

    __instance = None
    __hostname = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Server, cls).__new__(
                    cls, *args, **kwargs
            )
        try:
            Server.__hostname = socket.getfqdn()
        except:
            pass
        return cls.__instance

    def get_fqdn(self):
        if not self.__hostname:
            return 'N/A'
        else:
            return self.__hostname

    def get_ip(self):
        if self.__hostname:
            try:
                return socket.gethostbyname(self.__hostname)
            except:
                pass
        return 'N/A'

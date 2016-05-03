#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from bluebird.server.helper.registry import error


class NoAuthModule(Exception):

    def __init__(self):
        self.__registry = 'BluebirdServer'
        self.__message = 'NoAuthenticationModule'

    def __str__(self):
        return repr("{}: {}".format(self.__registry, self.__message))

    def response(self):
        return (error(self.__registry, self.__message), 500)


class NoValidSession(Exception):

    def __init__(self):
        self.__registry = 'Base'
        self.__message = 'NoValidSession'

    def __str__(self):
        return repr("{}: {}".format(self.__registry, self.__message))

    def response(self):
        return (error(self.__registry, self.__message), 403)


class SessionLimitExceeded(Exception):

    def __init__(self):
        self.__registry = 'Base'
        self.__message = 'SessionLimitExceeded'

    def __str__(self):
        return repr("{}: {}".format(self.__registry, self.__message))

    def response(self):
        return (error(self.__registry, self.__message), 403)

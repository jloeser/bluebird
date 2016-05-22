#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import base64
import logging
from datetime import datetime
from datetime import timedelta
from hashlib import md5
from time import time

from bluebird.server.sessions.exceptions import NoAuthModule
from bluebird.server.sessions.exceptions import NoValidSession
from bluebird.server.sessions.exceptions import SessionLimitExceeded

logger = logging.getLogger('session')


class BluebirdAuthentication():

    def authenticate(self, username, password):
        pass


class Session():

    __shared_state = {}
    # according to SessionService.1.0.0, timeout mus be between 30 and 86400
    __session_timeout_min = 30
    __sessions = {}
    __limit = 10
    __id = 0
    __authentication_instance = None

    def __init__(self):
        self.__dict__ = Session.__shared_state

    def get_timeout():
        return Session.__session_timeout_min

    def get_sessions():
        return Session.__sessions.keys()

    def check_xauth(self, xauth):
        for id, data in self.__sessions.items():
            if data['X-AUTH'] == xauth:
                current = datetime.now()
                timestamp = datetime.fromtimestamp(data['TIME'])
                if (current - timestamp) <\
                        timedelta(minutes=self.__session_timeout_min):

                    logger.debug("'{}' is valid.".format(xauth))
                    data['TIME'] = time()
                    data['USERNAME'] = data['USERNAME']
                    data['ID'] = id
                    return data
                else:
                    logger.debug("Session expired.")
                    del self.__sessions[id]
                    break

        logger.debug("'{}' is invalid.".format(xauth))
        return False

    def check_basic_auth(self, basic_auth):
        if not self.__authentication_instance:
            raise NoAuthModule

        prefix, credential = basic_auth.split(' ')
        if prefix == 'Basic':
            credential = base64.b64decode(credential).decode('utf-8')
            username, password = credential.split(':')
            if self.__authentication_instance.authenticate(
                    username, password):
                result = {
                        'USERNAME': username,
                        'PASSWORD': password
                }
                return result
        raise NoValidSession

    def create(self, username, password):
        if not self.__authentication_instance:
            raise NoAuthModule

        if self.__authentication_instance.authenticate(username, password):

            # check if a session is active for username and return same session
            for id, session in self.__sessions.items():
                if session['USERNAME'] == username:
                    logger.debug('Session already exists!')
                    return {
                            'ID': id,
                            'USERNAME': session['USERNAME'],
                            'X-AUTH': session['X-AUTH']
                    }

            # create new session if limit isn't reached
            if self.__id < self.__limit:
                id = md5(str.encode(str(self.__id)))
                id = id.hexdigest()
                current = time()
                xauth = md5()
                # TODO: use server key
                xauth.update(str.encode(str(current)))
                xauth = xauth.hexdigest()
                result = {
                        'ID': id,
                        'USERNAME': username,
                        'X-AUTH': xauth,
                }
                self.__sessions[id] = {
                        'USERNAME': username,
                        'PASSWORD': password,
                        'X-AUTH': xauth,
                        'TIME': current
                }
                self.__id += 1
                return result
            else:
                raise SessionLimitExceeded
        else:
            raise NoValidSession

    def delete(self, id):
        """Delete a session."""
        if id in self.__sessions.keys():
            del self.__sessions[id]

    def set_authentication_instance(instance):
        """
        Set the authentication instance; must be a subclass of
        BluebirdAuthentication.
        """
        if isinstance(instance, BluebirdAuthentication):
            Session.__dict__['_Session__shared_state']\
                    ['_Session__authentication_instance'] = instance
        else:
            raise TypeError

    def get_authentication_name(self):
        """Get the name of the authentication instance."""
        return self.__authentication_instance.__class__.__name__

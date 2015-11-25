#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import logging
import base64
from hashlib import md5
from time import time
from datetime import datetime, timedelta
from rfserver.server.authentication.user import User

logger = logging.getLogger('session')

class Session():

    _instance = None
    _initialized = False
    # according to SessionService.1.0.0, timeout mus be between 30 and 86400
    _session_timeout_min = 30
    _sessions = {}
    _id = 0

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Session, cls).__new__(
                    cls, *args, **kwargs
            )
        return cls._instance

    def __init__(self):
        if not Session._initialized:
            logger.debug(" * Sessions initialized.")
            Session._initialized = True

    def get_timeout():
        return Session._session_timeout_min

    def get_sessions():
        return Session._sessions.keys()

    def check_xauth(self, xauth):
        for id, data in self._sessions.items():
            if data['X-AUTH'] == xauth:
                current = datetime.now()
                timestamp = datetime.fromtimestamp(data['TIME'])
                if (current - timestamp) < timedelta(minutes=self._session_timeout_min):
                    logger.debug("'{}' is valid.".format(xauth))
                    data['TIME'] = time()
                    data['USERNAME'] = data['USERNAME']
                    data['ID'] = id
                    return data
                else:
                    logger.debug("Session expired.")
                    del self._sessions[id]
                    break

        logger.debug("'{}' is invalid.".format(xauth))
        return False

    def check_basic_auth(self, basic_auth):
        prefix, credential = basic_auth.split(' ')
        if prefix == 'Basic':
            credential = base64.b64decode(credential).decode('utf-8')
            username, password = credential.split(':')
            if User.is_authenticated(username, password):
                return True
        return False

    def create(self, username, password):
        if User.is_authenticated(username, password) and self._id < 10:
            id = md5(str.encode(str(self._id)))
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
            self._sessions[id] = {
                    'USERNAME': username,
                    'X-AUTH': xauth,
                    'TIME': current
            }
            self._id += 1
            return result
        else:
            return False

    def delete(self, id):
        if id in self._sessions.keys():
            del self._sessions[id]
        return True

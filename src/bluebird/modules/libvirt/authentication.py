#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import logging

from simplepam import authenticate as pam_authenticate

from bluebird.server.sessions.models import BluebirdAuthentication

from . import NAME

logger = logging.getLogger(NAME)


class SASL(BluebirdAuthentication):
    """
    Simple Authentication and Security Layer (SASL).
    """
    pass


class LocalUser(BluebirdAuthentication):
    """
    Check for local unix users on the host system. This module asks PAM for
    user authentication.
    """

    def authenticate(self, username, password):
        """
        Authenticates a local user on the system.

        Args:
            username (str): username of a local user
            password (str): clear text password for local user

        Returns:
            bool: either True or False if a given user was successfully
                authenticated or not
        """
        if pam_authenticate(username, password):
            logger.debug("Access granted for user '{}'".format(username))
            return True

        logger.debug("Authentication failure for user '{}'".format(username))
        return False

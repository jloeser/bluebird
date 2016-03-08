#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from bluebird.server.sessions.models import BluebirdAuthentication
from subprocess import PIPE, Popen, TimeoutExpired, CalledProcessError
from subprocess import STDOUT, check_output
from rflibvirt import NAME
import logging

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

    __cmd = '/sbin/unix2_chkpwd'
    __cmd_timeout_sec = 1

    def is_authenticated(self, username, password):
        """
        Authenticates a local user on the system.

        param: username -- str; username of a local user
        param: password -- str; clear text password for local user

        return: bool -- return either True or False if a given user was
                        successfully authenticated or not
        """
        try:
            echo = Popen(('echo', '-n', password), stdout=PIPE)

            unix2_chkpwd = check_output(
                    (LocalUser.__cmd, 'login', username),
                    stdin=echo.stdout,
                    timeout=LocalUser.__cmd_timeout_sec
            )

        except TimeoutExpired as e:
            logger.warning(
                    "{} timeout expired -> Access denied!"
                    .format(LocalUser.__cmd)
            )
            return False
        except CalledProcessError as e:
            logger.warning("Access denied!")
            return False
        except Exception as e:
            logger.warning(
                    "Unknown exception; return code {} ({}) -> Access denied!"
                    .format(e.returncode, LocalUser.__cmd)
            )
            return False

        logger.info("Access granted for user '{}'.".format(username))
        return True

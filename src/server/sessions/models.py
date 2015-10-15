#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import log

logger = log.getLogger('session')
logger.setLevel(log.getLogger().getEffectiveLevel())

class Session():

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Session, cls).__new__(
                    cls, *args, **kwargs
            )
        return cls._instance

    def __init__(self):
        if not Session._initialized:
            logger.debug("Initialized.")
            Session._initialized = True

    def is_valid(self, xauth):
        logger.debug("Session is valid.")
        return True

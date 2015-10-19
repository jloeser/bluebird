#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import sys
import config
import logging

if __name__ == '__main__':
    print("Error: module must be imported")
    sys.exit(1)

_loggers = []
_level = None

def get_logger(name=config.LOGGER['NAME'], level=config.LOGGER['LEVEL']):
    """
    Register a new Logger object.

    As long as global _level variable is None, we use the level parameter for
    the log level to be set.

    param: name -- name of the Logger
    param: level -- log level

    return: logging.Logger()
    """
    logging.setLoggerClass(Logger)
    logger = logging.getLogger(name)
    _loggers.append(logger)

    if _level:
        for logger in _loggers:
            logger.setLevel(_level)
    else:
        logger.setLevel(level)

    return logger

def set_level(level):
    """
    Set level for all registered Logger and set global _level variable for
    new Loggers in the future.

    param: level -- log level
    """
    global _level
    _level = level
    for logger in _loggers:
        logger.setLevel(_level)

class Logger(logging.Logger):

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

        # console output
        console = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s[%(name)s] %(message)s')
        console.setFormatter(formatter)
        self.addHandler(console)


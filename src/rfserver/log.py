#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import sys
import logging
from rfserver import config

if __name__ == '__main__':
    print("Error: module must be imported")
    sys.exit(1)

class Logger(logging.Logger):

    _logger = []
    _level = None

    def __init__(self, name):
        self._logger.append(self)
        logging.Logger.__init__(self, name, logging.DEBUG)

        # console output
        console = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s[%(name)s] >> %(message)s')
        console.setFormatter(formatter)
        self.addHandler(console)

    def set_global_level(self, level):
        self._level = level
        for logger in self._logger:
            logger.setLevel(level)

    def get_global_level(self):
        return self._level

logging.setLoggerClass(Logger)

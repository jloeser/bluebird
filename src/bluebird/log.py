#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import logging
import sys

if __name__ == '__main__':
    print("Error: module must be imported")
    sys.exit(1)


# https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
class esc:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger(logging.Logger):

    __logger = []
    __level = None

    def __init__(self, name):
        self.__logger.append(self)
        logging.Logger.__init__(self, name, logging.DEBUG)

        logging.addLevelName(
                logging.DEBUG, 'DD'
        )
        logging.addLevelName(
                logging.INFO, esc.BOLD + 'II' + esc.ENDC
        )
        logging.addLevelName(
                logging.WARNING, esc.WARNING + 'WW' + esc.ENDC
        )
        logging.addLevelName(
                logging.ERROR, esc.FAIL + esc.BOLD + 'EE' + esc.ENDC
        )

        # console output
        console = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
                '{asctime} {levelname} [{name:<8}] >> {message}',
                "%Y-%m-%d %H:%M:%S", style='{')
        console.setFormatter(formatter)
        self.addHandler(console)

    def set_global_level(self, level):
        self.__level = level
        for logger in self.__logger:
            logger.setLevel(level)

    def get_global_level(self):
        return self.__level

logging.setLoggerClass(Logger)

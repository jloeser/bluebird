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

def getLogger(name=config.LOGGER['NAME']):
    logging.setLoggerClass(Logger)
    logger = logging.getLogger(name)
    return logger

class Logger(logging.Logger):

    def __init__(self, name, level=config.LOGGER['LEVEL']):
        logging.Logger.__init__(self, name, logging.DEBUG)
        self.setLevel(level)

        # console output
        console = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s[%(name)s] %(message)s')
        console.setFormatter(formatter)
        self.addHandler(console)


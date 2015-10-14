#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import sys
if not sys.version_info[0] >= 3:
    print("Python 3 required! Exit.")
    sys.exit(1)
import config
import log
from importlib import import_module
from flask import Flask
import argparse
from server import app

logger = log.getLogger()

def probe_modules():
    # TODO: probe for installed modules
    modules = ['modules.libvirt']
    return modules

def main(module):
    try:
        system = import_module(module)
        logger.debug("Module '{}' found.".format(
                system.NAME
        ))
    except ImportError:
        logger.error("Couldn't find module '{}'. Exit.".format(
            module
        ))
        sys.exit(1)

    app.register_blueprint(system.views.module)
    app.config.from_object(config)
    if app.config['SERVER']['DEBUG']:
        app.config['DEBUG'] = True
    app.run()

if __name__ == '__main__':

    # define and handle arguments
    parser = argparse.ArgumentParser(
            prog=config.PROGRAM_NAME,
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False
    )
    parser.add_argument(
            'module',
            nargs='?',
            default='modules.libvirt',
            help="Specify the backend module. If no module is\n\
specified, the first one gets taken. Following\n\
modules have been found:\n\n{}".format('\n'.join(probe_modules()))
            )
    parser.add_argument(
            '-h',
            '--help',
            action="store_true",
            help="Show this help message and exit."
    )
    parser.add_argument(
            '-v',
            '--version',
            action="version",
            version="Copyright (c) 2015 SUSE LINUX GmbH\n{} v{}".format(
                    config.PROGRAM_NAME, config.PROGRAM_VERSION
            ),
            help="Show version."
    )
    parser.add_argument(
            '-d',
            '--debug',
            action="store_true",
            help="Show debug messages."
    )

    args = parser.parse_args()

    # show help message
    if args.help:
        parser.print_help()
        sys.exit(0)

    # enable debug messages
    if args.debug:
        logger.setLevel('DEBUG')

    main(args.module)

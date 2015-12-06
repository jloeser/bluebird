#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import sys
from rfserver import log

from rfserver import config
from rfserver.server import app

from importlib import import_module
from flask import Flask
import argparse
import logging

logger = logging.getLogger('main')

def probe_modules():
    """
    Probe for available modules on the system.

    return: [] -- list of str which can be imported via import_module()
    """
    # TODO: probe for installed modules
    modules = ['rflibvirt']
    return modules

def start(module, use_ssl=True):
    """
    Main function.

    Import the selected module as backend for the server and start the
    webserver.

    param: module -- str; backend module to be used
    param: use_ssl -- bool; activates/deactivates SSL support (default True)
    """
    try:
        system = import_module(module)
        logger.debug(" * Module '{}' found.".format(
                system.NAME
        ))
    except ImportError as e:
        logger.error(str(e))
        logger.error("Couldn't import module '{}'. Exit.".format(
            module
        ))
        sys.exit(1)

    app.config['MODULE'] = system.NAME
    app.register_blueprint(system.views.module)
    app.config.from_object(config)
    if app.config['SERVER']['DEBUG']:
        app.config['DEBUG'] = True

    if use_ssl:
        encryption = (config.SERVER['SSL_CRT'], config.SERVER['SSL_KEY'])
    else:
        logger.warning("No SSL encryption!")
        encryption = None

    app.run(
            host=config.SERVER['ADDRESS'],
            port=config.SERVER['PORT'],
            ssl_context=encryption
    )

def run():
    """
    Parse command line arguments and call main function.
    """

    parser = argparse.ArgumentParser(
            prog=config.PROGRAM_NAME,
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False
    )
    parser.add_argument(
            'module',
            nargs='?',
            default='rflibvirt',
            help="Specify the backend module. If no module is\n\
specified, the first one gets taken. Following\n\
modules have been found:\n\n{}".format('\n'.join(probe_modules()))
            )
    parser.add_argument(
            '-h',
            '--help',
            action='store_true',
            help="Show this help message and exit."
    )
    parser.add_argument(
            '-v',
            '--version',
            action='version',
            version="Copyright (c) 2015 SUSE LINUX GmbH\n{} v{}".format(
                    config.PROGRAM_NAME, config.PROGRAM_VERSION
            ),
            help="Show version."
    )
    parser.add_argument(
            '-d',
            '--debug',
            action='store_true',
            help="Show debug messages."
    )
    parser.add_argument(
            '--no-ssl',
            action='store_true',
            help="Disable SSL encryption."
    )

    args = parser.parse_args()

    # show help message
    if args.help:
        parser.print_help()
        sys.exit(0)

    # enable debug messages
    if args.debug:
        logger.set_global_level('DEBUG')
    else:
        logger.set_global_level(config.LOGGER['LEVEL'])

    start(args.module, use_ssl=not args.no_ssl)

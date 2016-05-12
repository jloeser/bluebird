#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import argparse
import logging
import os
import sys
from importlib import import_module

from bluebird import core
from bluebird.server import app
from bluebird.version import __version__

logger = logging.getLogger(core.PROGRAM_NAME_SHORT)

MODULES_DIR = 'bluebird.modules.'


def probe_modules():
    """
    Probe for available modules on the system.

    return: [] -- list of str which can be imported via import_module()
    """
    modules = []
    base_dir = os.path.dirname(__file__)
    for directory in os.listdir(base_dir + '/modules'):
        try:
            system = import_module(MODULES_DIR + directory)
            assert system.NAME
            assert system.views
            modules.append(system.NAME)
        except AttributeError:
            pass

    return modules


def start(module, use_ssl=True, use_wsgi_debugger=False):
    """
    Main function.

    Import the selected module as backend for the server and start the
    webserver.

    param: module -- str; backend module to be used
    param: use_ssl -- bool; activates/deactivates SSL support (default True)
    """
    try:
        if not module.startswith(MODULES_DIR):
            module = MODULES_DIR + module

        system = import_module(module)
        logger.debug(" * Module '{}' found.".format(
                system.NAME
        ))

        app.config['MODULE'] = system.NAME
        app.register_blueprint(system.views.module)
    except Exception as e:
        logger.error(str(e))
        logger.error("Couldn't import module '{}'. Exit.".format(
            module
        ))
        sys.exit(1)

    app.config.from_object(core)
    app.config['DEBUG'] = use_wsgi_debugger

    if use_ssl:
        encryption = (core.SERVER['SSL_CRT'], core.SERVER['SSL_KEY'])
    else:
        logger.warning("No SSL encryption!")
        encryption = None

    logger.info(" *** {} started... ".format(core.PROGRAM_NAME.title()))

    app.run(
            host=core.SERVER['ADDRESS'],
            port=core.SERVER['PORT'],
            ssl_context=encryption
    )


def run():
    """Parse command line arguments and call main function"""

    parser = argparse.ArgumentParser(
            prog=core.PROGRAM_NAME,
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False
    )
    parser.add_argument(
            'module',
            nargs='?',
            default=MODULES_DIR + 'libvirt',
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
                    core.PROGRAM_NAME, __version__
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
            '--debug-wsgi',
            action='store_true',
            help="Show WSGI (werkzeug) debug messages."
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
        logger.set_global_level(core.LOGGER['LEVEL'])

    # enable debug messages (WSGI)
    if args.debug_wsgi:
        wsgi_debug = args.debug_wsgi
    else:
        wsgi_debug = core.SERVER['DEBUG']

    start(args.module, use_ssl=not args.no_ssl, use_wsgi_debugger=wsgi_debug)

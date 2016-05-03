#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
# from flask import
import json
import logging

from flask import current_app
from flask import render_template

logger = logging.getLogger('message')

REGISTRIES = {
        'Base': '/RegistryStore/registries/en/Base.json',
        'BluebirdServer': '/RegistryStore/registries/en/BluebirdServer.json'
}

CODE = 'BluebirdServer.0.10.ExtendedInfo'
TYPE = '/redfish/v1/$metadata#Message.1.0.0.Message'


def get_message(registry, id):
    if registry in REGISTRIES.keys():
        filename = current_app.static_folder + REGISTRIES[registry]
        try:
            with open(filename) as f:
                data_json = json.loads(f.read())

                version = data_json['Version'].split('.')
                prefix = data_json['RegistryPrefix']
                messages = data_json['Messages']

                message = messages[id]['Message']
                severity = messages[id]['Severity']
                resolution = messages[id]['Resolution']
        except IOError:
            logger.warning(
                    "Can't find registry file: '{}'".format(filename))
            return False
        except KeyError as e:
            logger.warning("Can't find {} in message '{}'!".format(e, id))
            return False

        message_id = "{}.{}.{}.{}".format(prefix, version[0], version[1], id)

        data = {}
        data['ID'] = message_id
        data['MESSAGE'] = message
        data['SEVERITY'] = severity
        data['RESOLUTION'] = resolution

        return data

    return False


def error(registry, id):
    message = get_message(registry, id)
    if message:
        return render_template(
                'Error.json', code=CODE, type=TYPE,
                message='See @Message.ExtendedInfo for more information.',
                errors=[message])

    return render_template(
            'Error.json', code="Base.1.0.GeneralError",
            message="A general error has occurred.")

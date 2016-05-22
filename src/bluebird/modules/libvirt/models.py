#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import logging

import libvirt

from bluebird.exceptions import NoSystemFound

from . import NAME
from . import MONITOR_URI
from . import MANAGE_URI

ACTIVE = 0
INACTIVE = 1

ACTIONS = {
        'On': 'create',
        'ForceOff': 'destroy'
}

DOMAIN_STATES = {
        libvirt.VIR_DOMAIN_RUNNING:  "running",
        libvirt.VIR_DOMAIN_BLOCKED:  "idle",
        libvirt.VIR_DOMAIN_PAUSED:   "paused",
        libvirt.VIR_DOMAIN_SHUTDOWN: "in shutdown",
        libvirt.VIR_DOMAIN_SHUTOFF:  "shut off",
        libvirt.VIR_DOMAIN_CRASHED:  "crashed",
        libvirt.VIR_DOMAIN_NOSTATE:  "no state"
}

NOT_AVAILABLE = "N/A"

logger = logging.getLogger(NAME)


class Domain(libvirt.virDomain):

    def __init__(self, domain):
        libvirt.virDomain.__init__(self, domain, domain._o)

    def __del__(self):
        pass

    def get_id(self):
        dom_id = self.ID()
        if dom_id == -1:
            return NOT_AVAILABLE
        else:
            return dom_id

    def get_power_state(self):
        if self.isActive():
            return "On"
        else:
            return "Off"

    def get_exact_power_state(self):
        state = self.info()[0]
        return DOMAIN_STATES[state]

    def get_number_virtual_cpus(self):
        return self.info()[3]

    def get_total_memory(self):
        return self.info()[1] / (1024*1024)

    def get_max_memory(self):
        return self.info()[1] / 1024

    def get_used_memory(self):
        return self.info()[2] / 1024

    def get_ostype(self):
        return self.OSType()


class LibvirtMonitor():

    __shared_state = {}
    __initialized = False

    def __init__(self, uri=MONITOR_URI):
        self.__dict__ = LibvirtMonitor.__shared_state

        if not LibvirtMonitor.__initialized:
            try:
                self.conn = libvirt.openReadOnly(uri)

                self.domains = {}
                logger.info(" * Running hypervisor: {0} {1}".format(
                        self.conn.getType(),
                        self._get_version_str(self.conn.getVersion())
                ))
                logger.info(" * Library: {}".format(
                        self._get_version_str(self.conn.getLibVersion())
                ))

                self.collect_domains()
                LibvirtMonitor.__initialized = True

            except libvirt.libvirtError:
                raise NoSystemFound

    def _get_version_str(self, version):
        if isinstance(version, int):
            version = str(version).split('0')
            version = list(filter(('').__ne__, version))
            return '.'.join(version)
        elif isinstance(version, str):
            return version
        else:
            raise TypeError

    def collect_domains(self):
        self.domains = {}
        if self.conn.listAllDomains():
            for domain in self.conn.listAllDomains():
                self.domains[domain.UUIDString()] = Domain(domain)

    def probe(self):
        self.collect_domains()
        logger.info(" * Definded domains: {}".format(len(self.domains)))

    def get_domains(self):
        return self.domains.values()

    def get_domain(self, name):
        for uuid, domain in self.domains.items():
            if domain.name() == name:
                return domain
        return None

    def valid_action(self, action):
        if action in ACTIONS.keys():
            return ACTIONS[action]
        return None


class LibvirtManage():

    def __init__(self, credentials, uri=MANAGE_URI):
        self.username = credentials[0]
        self.password = credentials[1]

        auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE],
                self._request_credentials, None]

        try:
            uri = uri.format(username=self.username)
            self.conn = libvirt.openAuth(uri, auth, 0)
        except (KeyError, IndexError):
            logger.debug("User not set")
        except libvirt.libvirtError as e:
            logger.error(e)

    def _request_credentials(self, credentials, user_data):
        for credential in credentials:
            if credential[0] == libvirt.VIR_CRED_AUTHNAME:
                credential[4] = self.username
            elif credential[0] == libvirt.VIR_CRED_PASSPHRASE:
                credential[4] = self.password
        return 0

    def reset(self, domain, reset_type):
        if reset_type not in ACTIONS:
            raise Exception

        target = None
        for dom in self.conn.listAllDomains():
            if dom.name() == domain:
                target = dom
                break

        if target:
            if reset_type in ACTIONS:
                execute = getattr(target, ACTIONS[reset_type])
                try:
                    execute()
                except libvirt.libvirtError as e:
                    if 'already running' not in str(e):
                        raise Exception
                    else:
                        pass

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import logging
import libvirt
from rflibvirt import NAME

LIBVIRT_URI = 'qemu:///system'
ACTIVE = 0
INACTIVE = 1

RESET = {
        'On': 'start',
        'ForceOff': 'destroy'
}

DOMAIN_STATES = {
        libvirt.VIR_DOMAIN_RUNNING  : "running",
        libvirt.VIR_DOMAIN_BLOCKED  : "idle",
        libvirt.VIR_DOMAIN_PAUSED   : "paused",
        libvirt.VIR_DOMAIN_SHUTDOWN : "in shutdown",
        libvirt.VIR_DOMAIN_SHUTOFF  : "shut off",
        libvirt.VIR_DOMAIN_CRASHED  : "crashed",
        libvirt.VIR_DOMAIN_NOSTATE  : "no state"
}

logger = logging.getLogger(NAME)

class Domain(libvirt.virDomain):

    def __init__(self, domain):
        libvirt.virDomain.__init__(self, domain, domain._o)

    def get_id(self):
        dom_id = self.ID()
        if dom_id == -1:
            return "N/A"
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

    def start(self):
        try:
            self.create()
        except libvirt.libvirtError as error:
            logger.error(error)

    def destroy(self):
        try:
            libvirt.virDomain.destroy(self)
        except libvirt.libvirtError as error:
            logger.error(error)



class Libvirt():

    _instance = None
    _initialized = False
    _conn = None
    _domains = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Libvirt, cls).__new__(
                    cls, *args, **kwargs
            )
        return cls._instance

    def __init__(self):
        if not Libvirt._initialized:
            try:
                self._conn = libvirt.open(LIBVIRT_URI)
            except libvirt.libvirtError:
                raise NoSystemFoundException

            if not self._conn:
                raise NoSystemFoundException

            self._domains = {}
            logger.info(" * Running hypervisor: {0} {1}".format(
                    self._conn.getType(),
                    self._get_version_str(self._conn.getVersion())
            ))
            logger.info(" * Library: {}".format(
                    self._get_version_str(self._conn.getLibVersion())
            ))

            self._probe()
            Libvirt._initialized = True

    def _collect_domains(self):
        if self._conn.listAllDomains():
            for domain in self._conn.listAllDomains():
                self._domains[domain.UUIDString()] = Domain(domain)

    def _probe(self):
        self._collect_domains()
        logger.info(" * Definded domains: {}".format(len(self._domains)))


    def _get_version_str(self, version):
        if isinstance(version, int):
           version = str(version).split('0')
           version = list(filter(('').__ne__, version))
           return '.'.join(version)
        elif isinstance(version, str):
            return version
        else:
            raise TypeError
    @property
    def domains(self):
        return self._domains

    def get_domains(self):
        return self._domains.values()

    def get_domain(self, name):
        for uuid, domain in self._domains.items():
            if domain.name() == name:
                return domain
        return None

    def start(self, uuid):
        pass

    def reboot(self, uuid):
        pass

    def shutdown(self, uuid):
        pass

    def destroy(self, uuid):
        pass

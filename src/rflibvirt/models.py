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

ACTIONS = {
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

NOT_AVAILABLE = "N/A"

logger = logging.getLogger(NAME)

class Domain(libvirt.virDomain):

    def __init__(self, domain, owner):
        libvirt.virDomain.__init__(self, domain, domain._o)
        self._owner = owner

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

    def get_owner(self):
        if self._owner:
            return self._owner
        else:
            return NOT_AVAILABLE

    def set_owner(self, username):
        self._owner = username

    def start(self, username):
        if username == self.get_owner():
            try:
                self.create()
                return True
            except libvirt.libvirtError as error:
                logger.error(error)
                return False
        else:
            logger.error("Permission denied for user '{}' ('{}').".format(
                    username, self.name())
            )
            return False

    def destroy(self, username):
        if username == self.get_owner():
            try:
                libvirt.virDomain.destroy(self)
                return True
            except libvirt.libvirtError as error:
                logger.error(error)
                return False
        else:
            logger.error("Permission denied for user '{}' ('{}').".format(
                    username, self.name())
            )
            return False



class LibvirtMonitor():

    __instance = None
    __initialized = False
    __conn = None
    __domains = {}

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(LibvirtMonitor, cls).__new__(
                    cls, *args, **kwargs
            )
        return cls.__instance

    def __init__(self):
        if not LibvirtMonitor.__initialized:
            try:
                self.__conn = libvirt.openReadOnly(LIBVIRT_URI)
            except libvirt.libvirtError:
                raise NoSystemFoundException

            if not self.__conn:
                raise NoSystemFoundException

            self.__domains = {}
            logger.info(" * Running hypervisor: {0} {1}".format(
                    self.__conn.getType(),
                    self.__get_version_str(self.__conn.getVersion())
            ))
            logger.info(" * Library: {}".format(
                    self.__get_version_str(self.__conn.getLibVersion())
            ))

            self.__initialized = True

    def __collect_domains(self):
        self.__domains = {}
        if self.__conn.listAllDomains():
            for domain in self.__conn.listAllDomains():
                owner = System.get_owner(domain.name())
                self.__domains[domain.UUIDString()] = Domain(domain, owner)

    def __get_version_str(self, version):
        if isinstance(version, int):
           version = str(version).split('0')
           version = list(filter(('').__ne__, version))
           return '.'.join(version)
        elif isinstance(version, str):
            return version
        else:
            raise TypeError

    def probe(self):
        self.__collect_domains()
        logger.info(" * Definded domains: {}".format(len(self.__domains)))

    @property
    def domains(self):
        return self.__domains

    def get_domains(self):
        return self.__domains.values()

    def get_domain(self, name):
        for uuid, domain in self.__domains.items():
            if domain.name() == name:
                return domain
        return None

    def valid_action(self, action):
        if action in ACTIONS.keys():
            return ACTIONS[action]
        return None


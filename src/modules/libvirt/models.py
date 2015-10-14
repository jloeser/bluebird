#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import libvirt
import log
from . import NAME

LIBVIRT_URI = 'qemu:///system'
ACTIVE = 0
INACTIVE = 1

logger = log.getLogger(NAME)
logger.setLevel(log.getLogger().getEffectiveLevel())

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
            logger.info("Running hypervisor: {0} {1}".format(
                    self._conn.getType(),
                    self._get_version_str(self._conn.getVersion())
            ))
            logger.debug("Library: {}".format(
                    self._get_version_str(self._conn.getLibVersion())
            ))

            self._probe()
            Libvirt._initialized = True

    def _collect_domains(self):
        if self._conn.listAllDomains():
            for domain in self._conn.listAllDomains():
                self._domains[domain.UUIDString()] =\
                        [domain, domain.ID(), domain.isActive()]

    def _probe(self):
        self._collect_domains()
        logger.debug("Definded domains: {}".format(len(self._domains)))


    def _get_version_str(self, version):
        if isinstance(version, int):
           version = str(version).split('0')
           version = list(filter(('').__ne__, version))
           return '.'.join(version)
        elif isinstance(version, str):
            return version
        else:
            raise TypeError

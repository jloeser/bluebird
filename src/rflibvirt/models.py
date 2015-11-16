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

logger = logging.getLogger(NAME)

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
                self._domains[domain.UUIDString()] = domain

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
        for uuid, domain in self._domains.items():
            yield domain

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

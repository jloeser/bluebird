#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import pytest
from core import PASS
from core import USER

from bluebird.server.sessions import models
from bluebird.server.sessions.exceptions import NoAuthModule


def test_session_instance():
    """
    Borg shall return same data.
    """
    instance1 = models.Session()
    instance2 = models.Session()
    assert instance1.__dict__ == instance2.__dict__


def test_create():
    session = models.Session()
    session._Session__authentication_instance = None

    pytest.raises(NoAuthModule, session.create, USER, PASS)

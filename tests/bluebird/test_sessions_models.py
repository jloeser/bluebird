#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import pytest
from core import PASS
from core import USER

from bluebird.server.sessions.models import Session
from bluebird.server.sessions.exceptions import NoAuthModule


@pytest.fixture(scope='function')
def session():
    return Session()


def test_session_instance():
    """Borg shall return same data."""
    instance1 = Session()
    instance2 = Session()
    assert instance1.__dict__ == instance2.__dict__


def test_create(session):
    """Test create function."""
    session._Session__authentication_instance = None
    pytest.raises(NoAuthModule, session.create, USER, PASS)


def test_get_timeout():
    assert Session.get_timeout() == Session._Session__session_timeout_min


def test_get_sessions():
    pass

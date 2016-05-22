#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
import json

from flask import Blueprint
from flask import g
from flask import make_response
from flask import render_template
from flask import request

from bluebird.core import URL
from bluebird.server.decorators import collection
from bluebird.server.helper.registry import error
from bluebird.server.sessions.decorators import login_required
from bluebird.server.sessions.decorators import xauth_required
from bluebird.server.sessions.exceptions import NoAuthModule
from bluebird.server.sessions.exceptions import NoValidSession
from bluebird.server.sessions.exceptions import SessionLimitExceeded
from bluebird.server.sessions.models import Session

module = Blueprint('sessions', __name__)


@module.route(URL['SESSIONS'], methods=['POST'])
def create_session():
    try:
        data = json.loads(request.data.decode('utf-8'))
        assert 'UserName' and 'Password' in data

        result = g.session.create(
                username=data['UserName'],
                password=data['Password']
        )

        response = make_response(
                render_template('sessions/Session.1.0.0.json',
                                id=str(result['ID']),
                                username=result['USERNAME']
                                ), 201,
        )

        response.headers['Location'] = URL['SESSIONS'] + '/' + str(result['ID'])

        response.headers['X-Auth-Token'] = result['X-AUTH']
        return response

    except (ValueError, TypeError, KeyError, AssertionError):
        return (error('Base', 'UnrecognizedRequestBody'), 400)

    except (NoAuthModule,
            NoValidSession,
            SessionLimitExceeded) as e:
        return e.response()


@module.route(URL['SESSIONS'], methods=['GET'])
@login_required
@collection.odata_query_parameters_not_implemented
def show_session_collection():
    return render_template('sessions/SessionCollection.json',
                           sessions=Session.get_sessions()
                           )


@module.route(URL['SESSIONS'] + '/<id>', methods=['GET'])
@xauth_required
def show_session(id):
    return render_template('sessions/Session.1.0.0.json',
                           id=str(g.login['ID']),
                           username=g.login['USERNAME']
                           )


@module.route(URL['SESSIONS'] + '/<id>', methods=['DELETE'])
def delete_session(id):
    g.session.delete(id)
    return ('', 200)


@module.route(URL['SESSIONSERVICE'], methods=['GET'])
@login_required
def show_sessionservice():
    return render_template('sessions/SessionService.1.0.0.json',
                           state='enabled',
                           health='OK',
                           session_timeout=Session.get_timeout()
                           )

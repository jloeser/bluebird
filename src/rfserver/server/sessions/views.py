#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from rfserver.config import URL
from rfserver.server.sessions.decorators import login_required,\
        xauth_required, basic_authentication_required
from rfserver.server.sessions.models import Session
import json
from flask import Blueprint, jsonify, g, request, abort, url_for, redirect,\
        make_response, render_template
from rfserver.server.decorators import collection
from rfserver.server.helper.registry import error

module = Blueprint('sessions', __name__)

@module.route(URL['SESSIONS'] + '/Sessions', methods=['POST'])
def create_session():
    try:
        data = json.loads(request.data.decode('utf-8'))
    except ValueError as e:
        return (error('Base', 'MalformedJSON'), 400)

    if 'UserName' in data.keys() and 'Password' in data.keys():
        result = g.session.create(
                username=data['UserName'],
                password=data['Password']
        )

        if isinstance(result, tuple):
            return (error(result[0], result[1]), result[2])

        if result:
            response = make_response(
                    render_template('sessions/Session.1.0.0.json',
                            id=str(result['ID']),
                            username=result['USERNAME']
                    ), 201,
            )
            response.headers['Location'] = URL['SESSIONS'] + '/Sessions/' +\
                    str(result['ID'])
            response.headers['X-Auth-Token'] = result['X-AUTH']
            return response

    return (error('RedfishServer', 'UnauthorizedLoginAttempt'), 401)

@module.route(URL['SESSIONS'] + '/Sessions', methods=['GET'])
@login_required
@collection.odata_query_parameters_not_implemented
def show_session_collection():
    return render_template('sessions/SessionCollection.json',
            sessions=Session.get_sessions()
    )

@module.route(URL['SESSIONS'] + '/Sessions/<id>', methods=['GET'])
@xauth_required
def show_session(id):
    return render_template('sessions/Session.1.0.0.json',
            id=str(g.login['ID']),
            username=g.login['USERNAME']
    )

@module.route(URL['SESSIONS'] + '/Sessions/<id>', methods=['DELETE'])
def delete_session(id):
    if g.session.delete(id):
        return ('', 200)
    else:
        abort(500)

@module.route(URL['SESSIONS'], methods=['GET'])
@login_required
def show_sessionservice():
    return render_template('sessions/SessionService.1.0.0.json',
            state='enabled',
            health='OK',
            session_timeout=Session.get_timeout()
    )

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from flask import Blueprint, jsonify, g, request, abort, url_for, redirect,\
        make_response, render_template
from config import URL
import json
from server.sessions.decorators import login_required

module = Blueprint('sessions', __name__)

@module.route(URL['SESSIONS'], methods=['POST'])
def create_session():
    data = json.loads(request.data.decode('utf-8'))

    if 'UserName' in data.keys() and 'Password' in data.keys():
        result = g.session.create(
                username=data['UserName'],
                password=data['Password']
        )
        if result:
            response = make_response(
                    render_template('sessions/session_created.json',
                            id=str(result['ID']),
                            username=result['USERNAME']
                    ), 201,
            )
            response.headers['Location'] = URL['SESSIONS'] + '/' + str(result['ID'])
            response.headers['X-Auth-Token'] = result['X-AUTH']
            return response

    abort(400)

@module.route(URL['SESSIONS'], methods=['GET'])
@login_required
def show_session():
    return render_template('sessions/session_show.json',
            id=g.login['ID'],
            username=g.login['USERNAME']
    )

@module.route(URL['SESSIONS'] + '/<id>', methods=['DELETE'])
def delete_session(id):
    if g.session.delete(id):
        return ('', 200)
    else:
        abort(500)


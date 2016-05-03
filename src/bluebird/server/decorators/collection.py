#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author Jan Löser <jloeser@suse.de>
# Published under the GNU Public Licence 2
from functools import wraps

from flask import request

from bluebird.server.helper.registry import error


def odata_query_parameters_not_implemented(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Return Not Implemented (501) if query parameters are given.

        When the resource addressed is a collection, the client can use the
        following paging query options to specify that a subset of the members
        be returned. These paging query options apply to the Members property
        of a collection resource.

        Query options:

        * http://collection?$skip=5
        * http://collection?$top=30
        """
        for parameter in request.args:
            if parameter.startswith('$'):
                return (error('Base', 'QueryNotSupported'), 501)
        return f(*args, **kwargs)
    return decorated_function

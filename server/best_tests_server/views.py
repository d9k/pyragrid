from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User
    )

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)

import pyramid.security as security

import transaction

@view_config(route_name='home', renderer='templates/index.jinja2')
def home_view(request):
    userid = security.authenticated_userid(request)
    username = User.by_id(userid).
    return {'username': username}

@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    return {}


@view_config(route_name='logout', renderer='templates/logout.jinja2')
def logout_view(request):
    try:
        # one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
        one = []
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'best_tests_server'}


@view_config(route_name='add_user', renderer='templates/default_page.jinja2')
def add_user_view(request):
    try:
        with transaction.manager:
            new_user = User(vk_id=1, name='Павел Дуров')
            DBSession.add(new_user)

        # one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'content': 'user added'}


@view_config(route_name='delete_user', renderer='templates/default_page.jinja2')
def delete_user_view(request):
    vk_id = request.matchdict['vk_id']
    if not vk_id:
        return HTTPBadRequest('vk_id must be specified')

    try:
        with transaction.manager:
            DBSession.query(User).filter(User.vk_id == vk_id).delete()
        # transaction.commit()

    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'content': 'user deleted'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_best_tests_server_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

# TODO login/logout http://docs.pylonsproject.org/projects/pyramid//en/latest/tutorials/wiki2/authorization.html


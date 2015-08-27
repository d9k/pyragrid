from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)
from pyramid.security import has_permission
# from pyramid.url import route_url
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


class BaseViews:
    def __init__(self, request):
        self.request = request
        self.user_id = None
        self.user = None
        self.logined = self.check_logined(self.request)

    def check_logined(self, request):
        self.user_id = security.authenticated_userid(request)
        if not self.user_id:
            return False
        self.user = User.by_id(self.user_id)
        if not self.user:
            return False
        return True


@view_defaults(route_name='home', permission='view')
class SiteViews(BaseViews):

    # def __init__(self, request):
    #     super.__init__(request)

    @view_config(route_name='home', renderer='templates/index.jinja2')
    def home_view(self):
        """:type User"""
        return {'username': self.user.name}


class AuthViews(BaseViews):
    # def __init__(self, request):
    #     super.__init__(request)

    @view_config(route_name='login', renderer='templates/login.jinja2')
    @forbidden_view_config(renderer='templates/login.jinja2')
    def login_view(self):
        login = ''
        password = ''
        message = ''
        if 'login_form_submit' in self.request.params:
            login = self.request.params['login']
            password = self.request.params['password']
            #TODO no by_username, but by_email or by_login!
            user = User.by_any(login)
            """:type User"""
            if user:
                if user.check_password(password):
                    headers = security.remember(self.request, user.id)
                    home = self.request.route_url('home')
                    return HTTPFound(location=home, headers=headers)
                else:
                    message = 'wrong password'
            else:
                message = 'no user with such username'

        return {'login': login, 'password': password, 'message': message}

    @view_config(route_name='logout', renderer='templates/logout.jinja2')
    def logout_view(self):
        headers = security.forget(self.request)
        loginpage = self.request.route_url('login', self.request)
        return HTTPFound(location=loginpage, headers=headers)

    @view_config(route_name='add_user', renderer='templates/default_page.jinja2')
    def add_user_view(self):
        try:
            with transaction.manager:
                # new_user = User(vk_id=1, name='Павел Дуров')
                # DBSession.add(new_user)
                new_user = User(vk_id=1146494, login='d9kd9k', name='Дмитрий Комаров', email='d9k@ya.ru')
                new_user.set_password('testpass');
                DBSession.add(new_user)

                # one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)
        return {'content': 'user added'}

    @view_config(route_name='delete_user', renderer='templates/default_page.jinja2')
    def delete_user_view(self):
        vk_id = self.request.matchdict['vk_id']
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


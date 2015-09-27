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
from .widgets import exception_for_form_field
from colanderalchemy import SQLAlchemySchemaNode

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)

from .forms import (
    LoginSchema, RegisterSchema
)

import deform
import colander
from colander import SchemaNode
from deform import Form, Button

import pyramid.security as security

import transaction
import dictalchemy.utils
import best_tests_server.helpers as helpers

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

        authed_user = None

        # TODO deferred validator doesn't work!
        # @colander.deferred
        # @staticmethod
        def validate_auth(form, values):
            nonlocal authed_user

            login = values.get('login')
            password = values.get('password')
            user = User.by_any(login)

            # TODO check
            # -cdunklau- : d9k_ so i'm thinking you just need to do
            # form['login'].error = colander.Invalid(form['login'], 'Unknown login')
            # and then raise deform.ValidationFailure(form, form.cstruct, None) or something

            if not user:
                raise exception_for_form_field(form, 'login', 'Пользователь не найден')
            if not user.check_password(password):
                raise exception_for_form_field(form, 'password', 'Неверный пароль')

            authed_user = user

        login_form = Form(
            LoginSchema(validator=validate_auth).bind(),
            buttons=[Button(name='login_form_submit', title='Вход')],
            # css_class='no-red-stars'
        )

        login_form.css_class += ' no-red-stars'

        if 'login_form_submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                login_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(rendered_login_form=e.render())

            if authed_user is not None:
                self.request.session.pop('new_password', None)
                headers = security.remember(self.request, authed_user.id)
                home = self.request.route_url('home')
                return HTTPFound(location=home, headers=headers)

        return dict(rendered_login_form=login_form.render())

    @view_config(route_name='register', renderer='templates/register.jinja2')
    def register_view(self):

        # def validate_register(form, values):
        #     pass

        register_form = Form(
            RegisterSchema(
                # validator=validate_register
            ).bind(),
            buttons=[Button(name='register_form_submit', title='Зарегистрировать')]
        )

        if 'register_form_submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                data = register_form.validate(controls)
            except deform.ValidationFailure as e:
                r = e.render()
                return dict(rendered_register_form=r)

            # TODO create new user

            # new_user = User(login='d9kd9k', name='Дмитрий Комаров', email='d9k@ya.ru')

            new_user = User()
            new_user.fromdict(data)
            if not new_user.name:
                new_user.name = new_user.login
            password = data.get('password')
            if not password:
                password = helpers.generate_password()
                self.request.session['new_password'] = password

            new_user.set_password(password)
            try:
                with transaction.manager:
                    DBSession.add(new_user)
            except DBAPIError:
                return Response(conn_err_msg, content_type='text/plain', status_int=500)
            success_location = self.request.route_url('register_success')
            return HTTPFound(location=success_location)

        return dict(rendered_register_form=register_form.render())

    @view_config(route_name='register_success', renderer='templates/register_success.jinja2')
    def register_success_view(self):
        # TODO show user name and email
        new_password = self.request.session.get('new_password')
        return dict(new_password=new_password)

    @view_config(route_name='logout', renderer='templates/logout.jinja2')
    def logout_view(self):
        headers = security.forget(self.request)
        login_page = self.request.route_url('login')
        return HTTPFound(location=login_page, headers=headers)

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


@view_defaults(permission='admin')
class AdminViews(BaseViews):
    @view_config(route_name='delete_user', renderer='templates/default_page.jinja2')
    def delete_user_view(self):

        try:
            with transaction.manager:
                any_data = self.request.matchdict.get('any_data')
                id_ = self.request.matchdict.get('id')
                """:type : User"""
                user = None
                if any_data:
                    # DBSession.query(User).filter(User.vk_id == vk_id).delete()
                    user = User.by_any(any_data)
                elif id_:
                    user = User.by_id(id_)
                else:
                    return HTTPBadRequest('can\'t find user: no data specified')

                if not user:
                    return HTTPBadRequest('can\'t find user')
                DBSession.delete(user)
                # transaction.commit()

        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)
        return {'content': 'user ' + user.name + ' deleted'}

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


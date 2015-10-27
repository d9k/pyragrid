from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from .models import (
    DBSession,
    User
)

from .base_views import (
    BaseViews,
    conn_err_msg
)

import transaction

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)

from sqlalchemy.exc import DBAPIError

from best_tests_server import helpers

from .widgets import exception_for_schema_field

from .forms import (
    LoginSchema, RegisterSchema
)

import deform
from deform import Form, Button
import pyramid.security as security

import dictalchemy.utils


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
            """:type : User"""
            user = User.by_any(login)

            # TODO check
            # -cdunklau- : d9k_ so i'm thinking you just need to do
            # form['login'].error = colander.Invalid(form['login'], 'Unknown login')
            # and then raise deform.ValidationFailure(form, form.cstruct, None) or something

            if not user:
                raise exception_for_schema_field(form, 'login', 'Пользователь не найден')
            if not user.check_password(password):
                raise exception_for_schema_field(form, 'password', 'Неверный пароль')
            if not user.email_checked:
                raise exception_for_schema_field(form, 'login', 'Email пользователя не подтверждён. Проверьте почтовый ящик') #TODO показывать email "в звёздочках"
            if not user.active:
                raise exception_for_schema_field(form, 'login', 'Аккаунт пользователя заблокирован')
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
                self.request.session.invalidate()
                headers = security.remember(self.request, authed_user.id)
                index = self.request.route_url('admin_index' if authed_user.is_admin() else 'index')
                return HTTPFound(location=index, headers=headers)

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
            dictalchemy.utils.fromdict(new_user, data)
            self.request.session.invalidate()
            if not new_user.name:
                new_user.name = new_user.login
            password = data.get('password')
            if not password:
                password = User.generate_password()
                self.request.session['new_password'] = password
            new_user.set_password(password)
            try:
                with transaction.manager:
                    DBSession.add(new_user)
            except DBAPIError:
                return Response(conn_err_msg, content_type='text/plain', status_int=500)

            helpers.send_html_mail(new_user.email, 'registered',
                                   {'user_name': new_user.name, 'password': password})

            new_user.initiate_email_check()
            try:
                with transaction.manager:
                    DBSession.add(new_user)
            except DBAPIError:
                return Response(conn_err_msg, content_type='text/plain', status_int=500)

            self.request.session['new_user_id'] = new_user.id
            success_location = self.request.route_url('register_success')
            return HTTPFound(location=success_location)

        return dict(rendered_register_form=register_form.render())

    @view_config(route_name='register_success', renderer='templates/register_success.jinja2')
    def register_success_view(self):
        # TODO show user name and email
        new_user_id = self.request.session.get('new_user_id')
        if new_user_id is None:
            return HTTPBadRequest('Регистрация не была произведена или завершилась ошибкой')
        user = User.by_id(new_user_id)
        if not User:
            return HTTPNotFound('Пользователь не найден')
        new_password = self.request.session.get('new_password', None)
        return dict(user_name=user.name, new_password=new_password)

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
                new_user.set_password('testpass')
                DBSession.add(new_user)

                # one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)
        return {'content': 'user added'}

    @view_config(route_name='email_check_code', renderer='templates/email_check_success.jinja2')
    def email_check_code(self):
        # TODO как-то обернуть все методы в проверку DBAPIError (м. б. мету какую добавить)
        email_check_code = self.request.matchdict.get('code')
        if not email_check_code:
            return HTTPBadRequest('Код не указан')
        user = DBSession.query(User).filter(
            User.email_check_code == email_check_code,
            User.email_checked == False
        ).first()
        if not user:
            return HTTPNotFound('Срок действия кода истёк либо код указан неверно')
        with transaction.manager:
            user.email_check_code = None
            user.email_checked = True
            user.active = True
            DBSession.add(user)
        return {'user_name': user.name}

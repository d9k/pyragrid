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
    BaseViews, conn_err_msg
)

from .admin_views import AdminViews

from pyramid_mailer.mailer import Mailer
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

import transaction

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)

from sqlalchemy.exc import DBAPIError

from pyragrid import helpers

from datatables import ColumnDT, DataTables


class Testiews(AdminViews):
    @view_config(route_name='test_mail', renderer='templates/test/test_base.jinja2')
    def test_mail_view(self):
        # try:
        # with transaction.manager:
        """ :type : Mailer """
        # mailer = self.request.registry['mailer']
        mailer = get_mailer(self.request)
        message = Message(subject="test pyramid email send",
                          sender="d9kd9k@gmail.com",
                          recipients=['d9k@ya.ru'],
                          body="test body")
        mailer.send(message)
        transaction.commit()
        # except:
        #     return {'content': 'Error on email sending'}
        # TODO test headers from view name
        return {'header': 'Test Email', 'content': 'Email sent (?)'}

    @view_config(route_name='test_render', renderer='templates/test/test_base.jinja2')
    def test_render_view(self):
        rendered_view = helpers.render_to_string('templates/test_render/test_render.jinja2', self.request, {})
        return {'header': 'Test Render', 'code_block': rendered_view}

    @view_config(route_name='test_notify', renderer='templates/test/test_notify.jinja2')
    def test_notify(self):
        return {'header': 'Test notify'}

    @view_config(route_name='test_view_notify', renderer='templates/test/test_base.jinja2')
    def test_view_notify(self):
        self.add_success_flash('Тестирование успеха')
        self.add_error_flash('Тестирование ошибки')
        self.add_success_flash('И снова успех!')
        return {'header': 'Test view notify'}

    @view_config(route_name='test_url', renderer='templates/test/test_url.jinja2')
    def test_url(self):
        return {'header': 'Test url'}

    @view_config(route_name='test_ajax', renderer='templates/test/test_ajax.jinja2')
    def test_ajax(self):
        if self.request.method == 'GET':
            counter = int(self.request.GET.get('counter', 0))
        else:
            counter = int(self.request.POST.get('counter', 0))
        counter += 1
        return dict(header='Test ajax', counter=counter)

    @view_config(route_name='test_redirect', renderer='templates/test/test_base.jinja2')
    def test_redirect(self):
        admin_url = self.request.route_url('admin_index')
        return HTTPFound(location=admin_url)

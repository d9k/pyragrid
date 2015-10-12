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

import best_tests_server.helpers as helpers


@view_defaults(permission='admin')
class AdminViews(BaseViews):

    @view_config(route_name='admin_index', renderer='templates/admin_index.jinja2')
    def admin_index_view(self):
        """:type User"""
        return {'username': self.user.name}

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

    @view_config(route_name='test_mail', renderer='templates/default_page.jinja2')
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
        return {'content': 'Email sent (?)'}

    @view_config(route_name='test_render', renderer='templates/default_page.jinja2')
    def test_render_view(self):
        rendered_view = helpers.render_to_string('templates/test/test.jinja2', self.request, {})
        return {'code_block': rendered_view}
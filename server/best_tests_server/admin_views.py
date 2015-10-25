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

from best_tests_server import helpers

from datatables import ColumnDT, DataTables


@view_defaults(permission='admin')
class AdminViews(BaseViews):

    @view_config(route_name='admin_index', renderer='templates/admin/admin_index.jinja2')
    def admin_index_view(self):
        return {'username': self.user.name}

    @view_config(route_name='admin_users', renderer='templates/admin/admin_users.jinja2')
    def admin_users_view(self):
        return {'username': self.user.name}

    @view_config(route_name='admin_users_grid', request_method='GET', renderer='json')
    def admin_users_grid_view(self):
        columns = [
            ColumnDT('id'),
            ColumnDT('login'),
            ColumnDT('name'),
            ColumnDT('email'),
            ColumnDT('email_checked'),
            ColumnDT('active')
        ]
        query = DBSession.query(User)
        # instantiating a DataTable for the query and table needed
        row_table = DataTables(self.request.GET, User, query, columns)

        # returns what is needed by DataTable
        result = row_table.output_result()
        result = helpers.datatables_result_add_fake_column(result)
        return result

    # @view_config(route_name='admin_user_disable')
    # def admin_user_disable_view(self):

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


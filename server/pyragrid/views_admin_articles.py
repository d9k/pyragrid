from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from .models import (
    DBSession,
    User,
    Article
)

from .views_base import (
    ViewsBase, conn_err_msg
)

from .views_admin import ViewsAdmin

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

from pyragrid import helpers, forms

from datatables import ColumnDT, DataTables

import deform

import dictalchemy.utils

from . import widgets
from .datatables_mod import DataTablesMod


class ViewsAdminArticles(ViewsAdmin):
    @view_config(route_name='admin_articles', renderer='templates/admin/admin_articles.jinja2')
    def admin_articles_view(self):
        return {}

    @view_config(route_name='admin_articles_grid', request_method='GET', renderer='json')
    def admin_articles_grid_view(self):
        columns = [
            ColumnDT('id'),
            ColumnDT('name'),
            ColumnDT('system_name'),
            ColumnDT('path'),
            ColumnDT('active_revision'),
            ColumnDT('active')
        ]
        query = DBSession.query(Article)
        # instantiating a DataTable for the query and table needed
        row_table = DataTablesMod(self.request.GET, Article, query, columns)

        # returns what is needed by DataTable
        result = row_table.output_result()
        result = helpers.datatables_result_add_fake_column(result)
        return result

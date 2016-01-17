from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from .db import (
    DBSession,
    User,
    Article
)

from .views_base import (
    ViewsBase, conn_err_msg
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

from pyragrid import helpers, forms

from datatables import ColumnDT, DataTables

import deform

import dictalchemy.utils

from . import widgets
from .datatables_mod import DataTablesMod


@view_defaults(permission='admin')
class ViewsAdmin(ViewsBase):

    @view_config(route_name='admin_index', renderer='templates/admin/admin_index.jinja2')
    def admin_index_view(self):
        return {}


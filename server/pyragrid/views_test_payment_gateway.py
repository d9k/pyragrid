from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config,
    notfound_view_config
)
from .helpers import check_dev_mode
from pyramid.security import has_permission
# from pyramid.url import route_url
from sqlalchemy.exc import DBAPIError

from .db import (
    Base,
    DBSession,
    User,
    Good,
    Order,
    OrderGood,
    db_save_model
)

from .forms import OneClickBuySchema

from colanderalchemy import SQLAlchemySchemaNode

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)

import deform
from deform import Form, Button

import transaction
import dictalchemy.utils
from pyragrid import helpers

from .forms import (
    ProfileEditSchema
)

from .views_base import (
    ViewsBase, conn_err_msg
)

from .widgets import FormMod
from webob.multidict import MultiDict


@view_defaults(route_name='index')
class ViewsTestPaymentGateway(ViewsBase):

    def __init__(self, request):
        super().__init__(request)

    @view_config(route_name='test_payment_gateway_proceed', renderer='templates/test_payment_gateway_proceed.jinja2')
    def view_proceed(self):
        if not check_dev_mode():
            return HTTPNotFound()
        # TODO
        pass

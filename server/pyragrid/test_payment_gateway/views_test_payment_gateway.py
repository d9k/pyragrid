from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config,
    notfound_view_config
)
from ..helpers import check_dev_mode
from pyramid.security import has_permission
# from pyramid.url import route_url
from sqlalchemy.exc import DBAPIError

from ..db import (
    Base,
    DBSession,
    User,
    Good,
    Order,
    OrderGood,
    db_save_model
)

from ..forms import OneClickBuySchema

from colanderalchemy import SQLAlchemySchemaNode

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)

from deform import Form, Button

import transaction
import dictalchemy.utils
from pyragrid import helpers

from ..forms import (
    ProfileEditSchema
)

from ..views_base import (
    ViewsBase, conn_err_msg
)

from ..widgets import FormMod
from webob.multidict import MultiDict

from .test_payment_result_form import (
    RESULT_SUCCESS,
    RESULT_ERROR,
    TestPaymentResultSchema
)


# @view_defaults(route_name='index')
class ViewsTestPaymentGateway(ViewsBase):

    def __init__(self, request):
        super().__init__(request)

    @view_config(
        route_name='test_payment_gateway_proceed',
        renderer='test_payment_gateway/test_payment_gateway_proceed.jinja2'
    )
    def view_proceed(self):
        if not check_dev_mode():
            return HTTPNotFound()

        test_payment_result_schema = TestPaymentResultSchema()

        submit_button_name = 'test_payment_result_submit'
        form_submitted = submit_button_name in self.request.params

        money_transaction_id = None
        if not form_submitted:
            money_transaction_id = self.request.POST.get('money_transaction_id')
            if money_transaction_id is None:
                return HTTPBadRequest('No money_transaction_id specified')

        test_payment_result_form = FormMod(
            test_payment_result_schema.bind(
                # TODO bind params
            ),
            buttons=[Button(name=submit_button_name, title='Do action')],
            # css_class='no-red-stars'
        )

        appstruct = dict()
        appstruct['money_transcation_id'] = money_transaction_id

        return dict(rendered_test_payment_result_form=test_payment_result_form.render(appstruct))

from .abstract_payment_client import AbstractPaymentClient
import pyramid.config
from .views_payment_test import (ViewsPaymentTestServer)
from pyramid.view import (
    view_config,
)
import pyramid.threadlocal
from pyramid.request import Request
from ..db import (MoneyTransaction, MoneyTransactionStatus, EnumMoneyTransactionStatus, EnumRequestMethod)
from .. import helpers

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)

RESULT_SUCCESS = 'success'
RESULT_ERROR = 'error'


class ViewsPaymentTestClient:
    def __init__(self, request):
        # TODO """:type self.request """
        self.request = request

    @view_config()
    def view_payment_client_notify(self):
        # self.request.
        post = self.request.POST
        payment_result = post.get('payment_result')
        money_transaction_id = post.get('money_transaction_id')
        if payment_result is None:
            raise HTTPBadRequest('payment_result must be specified')
        if money_transaction_id is None:
            raise HTTPBadRequest('money_transaction_id must be specified')
        money_transaction = MoneyTransaction.by_id(money_transaction_id)
        if money_transaction is None:
            raise HTTPBadRequest('money_transaction with id={id}'.format(id=money_transaction_id))
        payment_client_test = PaymentClientTest()
        if payment_result == RESULT_SUCCESS:
            pass
        elif payment_result == RESULT_ERROR:
            pass
        else:
            raise HTTPBadRequest('unknown payment_result={result}'.format(result=payment_result))


class PaymentClientTest (AbstractPaymentClient):
    for_dev_only = True
    caption = 'Test payment system'
    test_field = 0000
    route_payment_form = 'testPaymentSystem/paymentForm'
    route_payment_notify = 'paymentApi/testPaymentNotify'

    def create_payment_form(self, transaction: MoneyTransaction):
        request = pyramid.threadlocal.get_current_request()
        app_url = request.application_url
        redirect_url = app_url + '/' + self.route_payment_form
        if transaction.id is None:
            raise Exception('transaction.id not defined')
        request_data = dict(
            money_transaction_id=transaction.id
        )
        new_transaction_status = MoneyTransactionStatus(
            money_transaction_id=transaction.id,
            status=EnumMoneyTransactionStatus.redirect_to_payment_form,
            url=redirect_url,
            request_method=EnumRequestMethod.POST,
            request_data=request_data,
            user=transaction.user
        )
        transaction.status_append(new_transaction_status)
        return new_transaction_status

    @classmethod
    def on_class_load(cls, config: pyramid.config.Configurator):
        super(cls, cls).on_class_load(config)
        config.add_route('test_payment_form', cls.route_payment_form)
        config.add_route('test_payment_notify', cls.route_payment_notify)
        settings = config.registry.settings
        ViewsPaymentTestServer.notify_url = settings.get(ViewsPaymentTestServer.__name__+'.notify_url')
        config.add_view(
            ViewsPaymentTestServer,
            attr='view_payment_form',
            route_name='test_payment_form',
            renderer='payment_systems/test_payment_form.jinja2'
        )
        config.add_view(
            ViewsPaymentTestClient,
            attr='view_payment_client_notify',
            route_name='test_payment_notify',
            renderer='string'
        )


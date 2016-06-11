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

    @view_config(renderer='json')
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
        """:type money_transaction MoneyTransaction"""
        if money_transaction is None:
            raise HTTPBadRequest('money_transaction with id={id}'.format(id=money_transaction_id))
        payment_client_test = PaymentClientTest()
        if money_transaction.status in [
            EnumMoneyTransactionStatus.failed,
            EnumMoneyTransactionStatus.notification_received,
            EnumMoneyTransactionStatus.notification_answered
        ]:
            raise HTTPBadRequest('money_transaction with id={id} already processed status notify'.format(
                id=money_transaction_id
            ))
        if payment_result == RESULT_SUCCESS:
            payment_client_test.process_paid(money_transaction, self.request)
            return {'message': 'success processed'}
        elif payment_result == RESULT_ERROR:
            payment_client_test.process_payment_error(money_transaction, self.request)
            return {'message': 'error processed'}
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
        new_transaction_status = self.create_transaction_status(
            EnumMoneyTransactionStatus.redirect_to_payment_form,
            transaction
        )
        new_transaction_status.url = redirect_url
        new_transaction_status.request_method = EnumRequestMethod.POST
        new_transaction_status.request_data = request_data
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


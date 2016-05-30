from .abstract_payment_client import AbstractPaymentClient
import pyramid.config
from .views_payment_test import (ViewsPaymentTest)
from pyramid.view import (
    view_config,
)


class ViewsPaymentTestClient:
    def __init__(self, request):
        self.request = request

    @view_config()
    def view_payment_client_notify(self):
        return ''


class PaymentClientTest (AbstractPaymentClient):
    for_dev_only = True
    caption = 'Test payment system'
    test_field = 0000
    route_payment_form = 'testPaymentSystem/paymentForm'
    route_payment_notify = 'paymentApi/testPaymentNotify'

    @classmethod
    def on_class_load(cls, config: pyramid.config.Configurator):
        super(cls, cls).on_class_load(config)
        config.add_route('test_payment_form', cls.route_payment_form)
        config.add_route('test_payment_notify', cls.route_payment_notify)
        config.add_view(
            ViewsPaymentTest,
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


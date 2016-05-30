from .abstract_payment_client import AbstractPaymentClient
import pyramid.config


class PaymentClientTest (AbstractPaymentClient):
    for_dev_only = True
    caption = 'Test payment system'
    test_field = 0000
    payment_form_url = 'test_payment_system/payment_form'

    @classmethod
    def on_class_load(cls, config: pyramid.config.Configurator):
        super(cls, cls).on_class_load(config)



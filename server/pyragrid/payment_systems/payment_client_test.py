from .abstract_payment_client import AbstractPaymentClient


class PaymentClientTest (AbstractPaymentClient):
    for_dev_only = True
    caption = 'Test payment system'
    test_field = 0000

    def on_class_load(self):
        pass


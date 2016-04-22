from .payment_client_test import PaymentClientTest

import sys, inspect


PAYMENT_CLIENT_CLASS_NAME_PREFIX = 'PaymentClient'
PREFIX_LEN = len(PAYMENT_CLIENT_CLASS_NAME_PREFIX)
_paymentClientClasses = {}

for name, _class in inspect.getmembers(sys.modules[__name__]):
    """:var name str"""
    if inspect.isclass(_class):
        if (name.startswith(PAYMENT_CLIENT_CLASS_NAME_PREFIX)):
            # TODO check for_dev_only
            key = name[PREFIX_LEN:]
            key = key[:1].lower() + key[1:]
            _paymentClientClasses[key] = _class


def get_payment_client_by_name(name):
    _paymentClientClasses.get(name)


def get_payment_clients_names():
    return list(_paymentClientClasses.keys())


def get_payment_clients_captions():
    captions = {}
    for name in _paymentClientClasses:
        # key = name[:1].upper() + name[1:]
        # key = PAYMENT_CLIENT_CLASS_NAME_PREFIX + key
        captions[name] = _paymentClientClasses[name].caption
    return captions



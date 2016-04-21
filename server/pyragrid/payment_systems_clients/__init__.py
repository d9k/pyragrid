from .payment_client_test import PaymentClientTest

import sys, inspect


PAYMENT_CLIENT_CLASS_NAME_PREFIX = 'PaymentClient'


def get_payment_client_by_name():
    pass


def get_payment_clients_names():
    _classes = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            _classes.append(obj)
    for _class in _classes:
        pass
        # TODO cut name without PaymentClient, lowercase it
    # return names
    return _classes



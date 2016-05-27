# from .payment_client_test import PaymentClientTest

import sys
import inspect
import importlib
import inflection


PAYMENT_CLIENT_CLASS_NAME_PREFIX = 'PaymentClient'
PREFIX_LEN = len(PAYMENT_CLIENT_CLASS_NAME_PREFIX)
_paymentClientClasses = {}

# for name, _class in inspect.getmembers(sys.modules[__name__]):
#     """:var name str"""
#     if inspect.isclass(_class):
#         if (name.startswith(PAYMENT_CLIENT_CLASS_NAME_PREFIX)):
#             # TODO check for_dev_only
#             key = name[PREFIX_LEN:]
#             key = key[:1].lower() + key[1:]
#             _paymentClientClasses[key] = _class


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


def load_by_settings(settings):
    payment_systems_enabled = settings.get('payment_systems_enabled')
    if payment_systems_enabled is None:
        return

    payment_systems_enabled = payment_systems_enabled.split()

    for name in payment_systems_enabled:
        class_name = PAYMENT_CLIENT_CLASS_NAME_PREFIX + name[:1].upper() + name[1:]
        package_name = inflection.underscore(class_name)
        imported_module = importlib.import_module('.'+package_name, __package__)
        _paymentClientClasses[name] = getattr(imported_module, class_name)


# from .payment_client_test import PaymentClientTest

import sys
import inspect
import importlib
import inflection
from .abstract_payment_client import AbstractPaymentClient
from .const import (PAYMENT_CLIENT_CLASS_NAME_PREFIX)

PREFIX_LEN = len(PAYMENT_CLIENT_CLASS_NAME_PREFIX)

_payment_client_classes = {}
_payment_clients_settings = dict()

# for name, _class in inspect.getmembers(sys.modules[__name__]):
#     """:var name str"""
#     if inspect.isclass(_class):
#         if (name.startswith(PAYMENT_CLIENT_CLASS_NAME_PREFIX)):
#             # TODO check for_dev_only
#             key = name[PREFIX_LEN:]
#             key = key[:1].lower() + key[1:]
#             _paymentClientClasses[key] = _class


def get_payment_client_class_by_name(name):
    return _payment_client_classes.get(name)


# TODO send additional arguments to constructor/ set fields from arguments?
def get_payment_client_by_name(name):
    payment_client_class = get_payment_client_class_by_name(name)
    if payment_client_class is None:
        return None
    return payment_client_class()


def get_payment_clients_names():
    return list(_payment_client_classes.keys())


def get_payment_clients_captions():
    captions = {}
    for name in _payment_client_classes:
        # key = name[:1].upper() + name[1:]
        # key = PAYMENT_CLIENT_CLASS_NAME_PREFIX + key
        captions[name] = _payment_client_classes[name].caption
    return captions


def load_by_config(config):
    settings = config.registry.settings
    payment_systems_enabled = settings.get('payment_systems_enabled')
    if payment_systems_enabled is None:
        return

    for setting_name in settings.keys():
        setting_value = settings.get(setting_name)
        if setting_name.startswith(PAYMENT_CLIENT_CLASS_NAME_PREFIX):
            setting_name_parts = setting_name.split('.')
            class_name = setting_name_parts[0]
            class_field = setting_name_parts[1]
            class_field_value = setting_value
            if class_name not in _payment_clients_settings:
                _payment_clients_settings[class_name] = dict()
            _payment_clients_settings[class_name][class_field] = class_field_value

    payment_systems_enabled = payment_systems_enabled.split()

    for name in payment_systems_enabled:
        class_name = PAYMENT_CLIENT_CLASS_NAME_PREFIX + name[:1].upper() + name[1:]
        package_name = inflection.underscore(class_name)
        imported_module = importlib.import_module('.'+package_name, __package__)
        payment_client_class = getattr(imported_module, class_name)
        _payment_client_classes[name] = payment_client_class
        # TODO set fields from config
        payment_client_settings = _payment_clients_settings.get(class_name, {})
        for setting_name in payment_client_settings:
            setattr(payment_client_class, setting_name, payment_client_settings[setting_name])

        payment_client_class.on_class_load(config)

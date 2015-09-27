from pyramid.threadlocal import get_current_request
import string
import random


def get_setting(key, default_value=None):
    request = get_current_request()
    settings = request.registry.settings
    return settings.get(key, default_value)


def check_dev_mode():
    return get_setting('dev_mode', False)


def generate_password(length=None):
    if not length:
        length = int(get_setting('generate_password_length', 8))
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

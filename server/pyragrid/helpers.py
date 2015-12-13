from pyramid.threadlocal import get_current_request
import string
import random
import copy
# import ConfigParser
import configparser
import pyramid.path
import pyramid.renderers
import pyramid.interfaces
import pyramid.traversal
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
import transaction
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import json
import pyramid.threadlocal
import colander
import os.path


def get_setting(key, default_value=None):
    request = get_current_request()
    if request is None:
        settings = pyramid.threadlocal.get_current_registry().settings
    else:
        settings = request.registry.settings
    if settings is None:
        return None
    return settings.get(key, default_value)


def check_dev_mode():
    return get_setting('dev_mode', False)


def generate_password(length=None, include_upper_case=False):
    if not length:
        length = int(get_setting('generate_password_length', 8))
    chars = string.ascii_lowercase + string.digits
    if include_upper_case:
        chars += string.ascii_uppercase
    return ''.join(random.choice(chars) for _ in range(length))


# see http://stackoverflow.com/a/7205234/1760643
def dicts_merge(dictionary1, dictionary2):
    output = {}
    for item, value in dictionary1.items():
        if item in dictionary2:
            if isinstance(dictionary2[item], dict):
                output[item] = dicts_merge(value, dictionary2.pop(item))
        else:
            output[item] = value
    for item, value in dictionary2.items():
        output[item] = value
    return output


def dict_has_keys(_dict: dict, keys: list):
    """ see http://stackoverflow.com/a/1285920/1760643 """
    if not isinstance(_dict, dict):
        return False
    return all(k in _dict for k in keys)


def dict_has_data(_dict: dict, data_to_have: dict):
    if not isinstance(_dict, dict):
        return False
    has_data = True
    for key, value in data_to_have.items():
        if _dict.get(key) != value:
            has_data = False
            break
    return has_data


def dict_to_vars(_dict: dict, keys: list):
    for key in keys:
        yield _dict[key]


# see https://gist.github.com/mmerickel/7901444
def load_config(file_name):
    config = configparser.ConfigParser()
    config.read(file_name)
    # db_url = config.get('app:main', 'sqlalchemy.url')
    d = dict(config._sections)
    for k in d:
        d[k] = dict(config._defaults, **d[k])
        d[k].pop('__name__', None)
    return d


#TODO get_relative_config_path
def get_passwords_config_path(config_path):
    config_dir_path = os.path.dirname(config_path)
    config_file_name_with_ext = os.path.basename(config_path)
    config_file_name, config_file_ext = os.path.splitext(config_file_name_with_ext)
    passwords_config_name = config_file_name + '_passwords' + config_file_ext
    return os.path.abspath(os.path.join(config_dir_path, passwords_config_name))


def render_to_string(template_name, request, template_params):
    package = pyramid.path.caller_package()
    renderer = pyramid.renderers.RendererHelper(
        name=template_name,
        package=package,
        registry=request.registry)
    root_factory = request.registry.queryUtility(pyramid.interfaces.IRootFactory, default=pyramid.traversal.DefaultRootFactory)
    root = root_factory(request)
    traverser = request.registry.adapters.queryAdapter(root, pyramid.interfaces.ITraverser)
    if traverser is None:
        traverser = pyramid.traversal.ResourceTreeTraverser(root)
    tdict = traverser(request)
    context = tdict['context']
    # return renderer.render(template_params, request, context)
    # return renderer.render(template_params, None, context)
    return renderer.render(template_params, None, request)


def send_html_mail(recipient, template_short_name, template_params, subject=None):
    template_short_name = 'templates/mail/' + template_short_name + '.jinja2'
    request = get_current_request()
    rendered = render_to_string(template_short_name, request, template_params)
    if not subject:
        subject = get_setting('mail_default_subject', 'Default subject')
        html = BeautifulSoup(rendered, 'html.parser')
        h1 = html.find('h1')
        if h1:
            subject = h1.string
        # subject = h1[0] if len(h1) > 0 else default_subject
    with transaction.manager:
        mailer = get_mailer(request)
        message = Message(subject=subject,
                          recipients=[recipient],
                          html=rendered)
        mailer.send(message)


def datatables_result_add_fake_column(datatables_result):
    data = datatables_result.get('aaData')
    for i in range(len(data)):
        record_dict = data[i]
        max_key = int(max(record_dict.keys(), key=int))
        new_key = max_key + 1
        record_dict[str(new_key)] = ''
        data[i] = record_dict
    return datatables_result


def obj_set_fields_from_dict(obj, data_dict):
    for key in data_dict:
        if data_dict[key] == colander.null:
            setattr(obj, key, None)
        else:
            setattr(obj, key, data_dict[key])


def build_url(host_page_url: str, get_params: dict = None):
    if not get_params:
        return host_page_url
    return host_page_url + '?' + urllib.parse.urlencode(get_params)


def get_from_url(url: str, get_params: dict = None):
    full_url = build_url(url, get_params)
    responce = urllib.request.urlopen(full_url)
    data = responce.read()
    """ :type : bytes """
    result = None
    try:
        result = data.decode('utf-8')
    except:
        pass
    if result:
        return result
    # TODO import chardet.. http://stackoverflow.com/a/1495631/1760643
    result = data.decode('latin-1')
    return result


def get_json_from_url(url: str, get_params: dict = None):
    result = get_from_url(url, get_params)
    if not result:
        return {}
    try:
        return json.loads(result)
    except:
        return {}


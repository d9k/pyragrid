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


def get_setting(key, default_value=None):
    request = get_current_request()
    settings = request.registry.settings
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
    return renderer.render(template_params, None, context)



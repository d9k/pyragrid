import colander
import deform
import deform.widget
from deform.widget import CheckedInputWidget
import deform.compat
from colander import null, Invalid
from pyramid.threadlocal import get_current_request

from urllib.parse import urlencode, urlparse
import http.client

# @colander.deferred
# def deferred_recaptcha_widget(node, kw):
#     request = kw['request']

# from https://gist.github.com/reedobrien/701444
# TODO https://docs.python.org/3.2/library/http.client.html

from chameleon.utils import Markup
import re


class TextInputPlaceHolderWidget(deform.widget.TextInputWidget):
    placeholder = ''
    template = 'pyragrid:templates/deform_mod/textinputplaceholder.pt'

    def serialize(self, field, cstruct, **kw):
        if cstruct in (null, None):
            cstruct = ''
        readonly = kw.get('readonly', self.readonly)
        template = readonly and self.readonly_template or self.template
        values = self.get_template_values(field, cstruct, kw)
        # hack for placeholder working
        values['placeholder'] = self.placeholder
        return field.renderer(template, **values)


class PasswordPlaceholderWidget(TextInputPlaceHolderWidget):
    placeholder = ''
    template = 'pyragrid:templates/deform_mod/passwordplaceholder.pt'
    # TODO fix readonly
    readonly_template = 'readonly/password'
    redisplay = False


class RecaptchaWidget(CheckedInputWidget):
    """
    requirements: ini settings must have recaptcha_private_key, recaptcha_public_key records
    """
    # template = 'recaptcha_widget'
    template = 'pyragrid:templates/deform_mod/recaptcha_widget.pt'
    readonly_template = 'recaptcha_widget'
    requirements = ()
    url = "http://www.google.com/recaptcha/api/verify"
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    # TODO lang from request localizer
    lang = 'en'
    # see https://developers.google.com/recaptcha/old/docs/customization for theming
    theme = 'red'

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (null, None):
            cstruct = ''
        confirm = getattr(field, 'confirm', '')
        template = readonly and self.readonly_template or self.template
        request = get_current_request()
        settings = request.registry.settings
        return field.renderer(template, field=field, cstruct=cstruct,
                              public_key=settings['recaptcha_public_key'],
                              lang=self.lang,
                              theme=self.theme
                              )

    def deserialize(self, field, pstruct):
        if pstruct is null:
            return null
        challenge = pstruct.get('recaptcha_challenge_field') or ''
        response = pstruct.get('recaptcha_response_field') or ''
        if not response:
            raise Invalid(field.schema, 'No input')
        if not challenge:
            raise Invalid(field.schema, 'Missing challenge')
        request = get_current_request()
        settings = request.registry.settings
        privatekey = settings['recaptcha_private_key']
        remoteip = request.remote_addr
        data = urlencode(dict(privatekey=privatekey,
                              remoteip=remoteip,
                              challenge=challenge,
                              response=response))
        url_components = urlparse(self.url)
        h = http.client.HTTPConnection(url_components.netloc, timeout=10)
        try:
            h.request("POST", url_components.path,
                      body=data, headers=self.headers)
            resp = h.getresponse()
            content = resp.read()
        except AttributeError as e:
            if e=="'NoneType' object has no attribute 'makefile'":
                # TODO old code, fix
                ## XXX: catch a possible httplib regression in 2.7 where
                ## XXX: there is no connextion made to the socker so
                ## XXX sock is still None when makefile is called.
                raise Invalid(field.schema,
                              "Could not connect to the captcha service.")
        if not resp.status == 200:
            raise Invalid(field.schema,
                          "There was an error talking to the recaptcha \
                          server{0}".format(resp.status))
        content = content.decode('utf-8')
        valid, reason = content.split('\n')
        # resp.reason?
        if not valid == 'true':
            if reason == 'incorrect-captcha-sol':
                reason = "Incorrect solution"
            raise Invalid(field.schema, reason.replace('\\n', ' ').strip("'") )
        # return pstruct
        return pstruct['recaptcha_response_field']


def exception_for_schema_field(form, field_name: str, text: str):
    """
    draw exception near specific form field
    """""
    exc = colander.Invalid(form)
    """:type : SchemaNode"""
    # field = form.get(field_name)
    field = None
    field_pos = 0
    for pos, f in enumerate(form.children):
        if f.name == field_name:
            field = f
            field_pos = pos
            break

    exc.add(colander.Invalid(field, text), field_pos)
    return exc


class FormEx(deform.Form):
        def __init__(self, schema, action='', method='POST', buttons=(),
                 formid='deform', use_ajax=False, ajax_options='{}',
                 autocomplete=None, **kw):
            if autocomplete:
                autocomplete = 'on'
            elif autocomplete is not None:
                autocomplete = 'off'
            self.autocomplete = autocomplete
            deform.Field.__init__(self, schema, **kw)
            _buttons = []
            for button in buttons:
                if isinstance(button, deform.compat.string_types):
                    button = ButtonEx(button)
                _buttons.append(button)
            self.action = action
            self.method = method
            self.buttons = _buttons
            self.formid = formid
            self.use_ajax = use_ajax
            self.ajax_options = Markup(ajax_options.strip())
            form_widget = getattr(schema, 'widget', None)
            if form_widget is None:
                form_widget = FormWidgetEx()
            self.widget = form_widget


class FormWidgetEx(deform.widget.FormWidget):
    template = 'pyragrid:templates/deform_mod/form_mod.pt'
    # readonly_template = 'readonly/form'


class ButtonEx(deform.Button):
    """ + description (tooltip) """
    def __init__(self, name='submit', title=None, type='submit', value=None,
                 disabled=False, css_class=None, description=None):
        if title is None:
            title = name.capitalize()
        name = re.sub(r'\s', '_', name)
        if value is None:
            value = name
        self.name = name
        self.title = title
        self.type = type
        self.value = value
        self.disabled = disabled
        self.css_class = css_class
        self.description = description

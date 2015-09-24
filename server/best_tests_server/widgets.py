import colander
import deform
import deform.widget
from deform.widget import CheckedInputWidget
from colander import null, Invalid
from pyramid.threadlocal import get_current_request

from urllib.parse import urlencode, urlparse
import http.client

# @colander.deferred
# def deferred_recaptcha_widget(node, kw):
#     request = kw['request']

# from https://gist.github.com/reedobrien/701444
# TODO https://docs.python.org/3.2/library/http.client.html


class TextInputPlaceHolderWidget(deform.widget.TextInputWidget):
    placeholder = ''
    template = 'best_tests_server:templates/deform_mod/textinputplaceholder.pt'

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
    template = 'best_tests_server:templates/deform_mod/passwordplaceholder.pt'
    readonly_template = 'readonly/password'
    redisplay = False


class RecaptchaWidget(CheckedInputWidget):
    # template = 'recaptcha_widget'
    template = 'best_tests_server:templates/deform_mod/recaptcha_widget.pt'
    readonly_template = 'recaptcha_widget'
    requirements = ()
    url = "http://www.google.com/recaptcha/api/verify"
    # google_url = "http://www.google.com/recaptcha/api/verify"
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    # TODO lang from request localizer
    lang = 'en'
    theme = 'red'

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (null, None):
            cstruct = ''
        confirm = getattr(field, 'confirm', '')
        template = readonly and self.readonly_template or self.template
        request = get_current_request()
        settings = request.registry.settings
        return field.renderer(template, field=field, cstruct=cstruct,
                              public_key=settings['google_api_public_key'],
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
        privatekey = settings['private_key']
        # remoteip = self.request.remote_addr
        remoteip = request.remote_addr
        data = urlencode(dict(privatekey=privatekey,
                              remoteip=remoteip,
                              challenge=challenge,
                              response=response))
        url_components = urlparse(self.url)
        # h = httplib2.Http(timeout=10)
        h = http.client.HTTPConnection(url_components["host"], timeout=10)
        try:
            # resp, content = h.request(self.url,
            #                           "POST",
            #                           headers=self.headers,
            #                           body=data)
            h.request("POST", url_components["path"],
                      body=data, headers=self.headers)
            resp = h.getresponse()
            content = resp.read()
        except AttributeError as e:
            if e=="'NoneType' object has no attribute 'makefile'":
                ## XXX: catch a possible httplib regression in 2.7 where
                ## XXX: there is no connextion made to the socker so
                ## XXX sock is still None when makefile is called.
                raise Invalid(field.schema,
                              "Could not connect to the captcha service.")
        if not resp.status == '200':
            raise Invalid(field.schema,
                          "There was an error talking to the recaptcha \
                          server{0}".format(resp['status']))
        valid, reason = content.split('\n')
        # resp.reason?
        if not valid == 'true':
            if reason == 'incorrect-captcha-sol':
                reason = "Incorrect solution"
            raise Invalid(field.schema, reason.replace('\\n', ' ').strip("'") )
        return pstruct

from deform.widget import CheckedInputWidget
from pyramid.threadlocal import get_current_request

from urllib.parse import urlencode, urlparse
import http.client
# from https://gist.github.com/reedobrien/701444
# TODO https://docs.python.org/3.2/library/http.client.html
from colander import null, Invalid


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
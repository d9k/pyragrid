from .models import (
    DBSession,
    User
)
import pyramid.security as security
from pyramid.request import Request
from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound,
    HTTPServerError
)
from . import helpers
import hashlib
from pyramid.response import Response
from .models import (
    DBSession,
)
import transaction
from sqlalchemy.exc import DBAPIError


class ViewsBase:
    """
    :type user: User
    """

    def __init__(self, request):
        self.request = request
        """ :type : Request"""

        if self.request.matchdict is None:
            self.request.matchdict = dict()

        self.notfound = \
             request.exception is not None \
             and type(request.exception).__name__ == 'HTTPNotFound'

        self.user_id = None
        self.user = None
        self.ajax = self.request.is_xhr
        self.logined = self.check_logined(self.request)
        self.vk_id = self.check_vk_auth()
        self.login_from_vk_iframe = self.request.session.get('login_from_vk_iframe')
        self.pnotify = []


    def check_logined(self, request):
        self.user_id = security.authenticated_userid(request)
        if not self.user_id:
            return False
        self.user = User.by_id(self.user_id)
        if not self.user:
            return False
        return True

    def check_vk_auth(self):
        # vk_auth_key = self.request.params.get('auth_key')
        # vk_auth_token = self.request.params.get('access_token')
        vk_id = self.request.session.get('vk_id')

        # if not vk_auth_key or not vk_auth_token or not vk_id:
        if not vk_id:
            # return HTTPBadRequest('нет входных параметров vk')
            return None  # not inside iframe

        if not self.user:
            return None

        if self.user.vk_id == vk_id:
            return vk_id

        return None

    def add_flash_message(self, title=None, text=None, type='success'):
        new_message = {}
        if title is not None:
            new_message['title'] = title
        if text is not None:
            new_message['text'] = text
        if type is not None:
            new_message['type'] = type
        self.pnotify.append(new_message)

    def add_success_flash(self, title=None, text=None):
        self.add_flash_message(title, text, 'success')

    def add_error_flash(self, title=None, text=None):
        self.add_flash_message(title, text, 'error')

    @staticmethod
    def db_error_response(error: Exception):
        return Response('Error ' + type(error).__name__ + "\n\n" + conn_err_msg,
                        content_type='text/plain',
                        status_int=500)


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyragrid_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

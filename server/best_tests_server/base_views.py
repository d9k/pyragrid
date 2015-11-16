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


class BaseViews:
    """
    :type user: User
    """
    def __init__(self, request):
        self.request = request
        """ :type : Request"""

        self.user_id = None
        self.user = None
        self.ajax = self.request.is_xhr
        self.logined = self.check_logined(self.request)
        self.vk_id = self.check_vk_auth()
        self.login_from_vk_iframe = self.request.session.get('login_from_vk_iframe')
        self.pnotify=[]
        a = 1

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
        #         headers = security.forget(self.request)
        #         # vk_page = self.request.route_url('vk_auth')
        #         return HTTPFound(location=self.request.url, headers=headers)
        #
        # vk_app_id_str = helpers.get_setting('vk_app_id')
        # vk_app_secret_key = helpers.get_setting('vk_app_secret_key')
        # vk_api_version = helpers.get_setting('vk_api_version')
        #
        # str_to_hash = vk_app_id_str + '_' + vk_id + '_' + vk_app_secret_key
        #
        # if hashlib.md5(str_to_hash.encode('utf-8')).hexdigest() != vk_auth_key:
        #     return HTTPBadRequest('Ошибка безопасности: vk_auth_key неверен')
        #
        # token_get_result = helpers.get_json_from_url('https://api.vk.com/oauth/access_token', dict(
        #     v=vk_api_version,
        #     client_id=vk_app_id_str,
        #     client_secret=vk_app_secret_key,
        #     grant_type='client_credentials',
        #     scope='offline'
        # ))
        #
        # access_token = token_get_result.get('access_token')
        # if not access_token:
        #     return HTTPServerError('Ошибка при получении серверного access_token')
        #
        # check_tocken_result = helpers.get_json_from_url('https://api.vk.com/method/secure.checkToken', dict(
        #     token=vk_auth_token,
        #     access_token=access_token,
        #     client_secret=vk_app_secret_key
        # ))
        #
        # check_tocken_response = check_tocken_result.get('response')
        # if not isinstance(check_tocken_response, dict):
        #     return HTTPServerError('Ошибка при проверке access_token: неверный формат ответа')
        #
        # success = check_tocken_response.get('success')
        # user_id = check_tocken_response.get('user_id')
        #
        # if not success == 1 or not user_id == int(vk_id):
        #     return HTTPServerError('Ошибка при проверке access_token: неверный формат ответа')
        #
        # # TODO find matching user
        # authed_user = User.by_vk_id(vk_id)
        #
        # if authed_user is not None:
        #     self.request.session.invalidate()
        #     headers = security.remember(self.request, authed_user.id)
        #     index = self.request.route_url('admin_index' if authed_user.is_admin() else 'index')
        #     return HTTPFound(location=index, headers=headers)
        #
        # # TODO or create new one
        # return vk_id

    def responce_db_error(self):
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

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

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_best_tests_server_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
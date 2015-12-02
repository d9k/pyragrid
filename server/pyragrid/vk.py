# vk helpers

from pyragrid import helpers
from . import helpers
import logging
import hashlib
from .models import User

log = logging.getLogger(__name__)

vk_app_secret_key = helpers.get_setting('vk_app_secret_key')
vk_app_id = helpers.get_setting('vk_app_id')
vk_api_version = helpers.get_setting('vk_api_version')
vk_api_method_url = 'https://api.vk.com/method/'


def get_token(scope='offline'):
    token_get_result = helpers.get_json_from_url('https://api.vk.com/oauth/access_token', dict(
        v=vk_api_version,
        client_id=vk_app_id,
        client_secret=vk_app_secret_key,
        grant_type='client_credentials',
        scope=scope
    ))
    return token_get_result.get('access_token')


def api_request(method:str, params:dict):
    # TODO log if error (example: {"error":{"error_code":113,"error_msg":"Invalid user id","request_params":[{"key":"oauth","value":"1"},{"key":"method","value":"users.get"},{"key":"uids","value":"ID_OR_NICK"},{"key":"fields","value":"photo_200,status"}]}})
    return helpers.get_json_from_url(vk_api_method_url+'/'+method, params)


def api_response(method:str, params:dict):
    result = api_request(method, params)
    response = result.get('response')
    if not isinstance(response, dict):
        if isinstance(response, list):
            try:
                r = response[0]
            except IndexError:
                r = None
            return r
        return None
    return response


def check_md5_vk_auth_key(vk_id, vk_auth_key):
    str_to_hash = vk_app_id + '_' + vk_id + '_' + vk_app_secret_key

    return hashlib.md5(str_to_hash.encode('utf-8')).hexdigest() == vk_auth_key


def update_user_model_by_vk_id(user, vk_id):
    user_info = api_response('users.get', dict(uids=vk_id, fields='screen_name,sex'))
    if helpers.dict_has_keys(user_info, ['first_name', 'last_name']):
        user.name = user_info['last_name'] + ' ' + user_info['first_name']
        if 'screen_name' in user_info:
            if User.by_login(user_info['screen_name']) is None:
                user.login = user_info['screen_name']

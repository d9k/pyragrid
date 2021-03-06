from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyragrid.templates.jac_compressors.babel_compressor import BabelCompressor

from .db import (
    DBSession,
    Base,
    User
)

from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request
from pkg_resources import resource_filename
import deform
from pyragrid import helpers

from pyramid_mailer.mailer import Mailer
import os.path
import pyramid.events
import pyramid_jinja2
import pyramid.threadlocal
import json

from . import views_articles

import os.path

from . import payment_systems

from jac.config import Config as JacDefaultConfig

# http://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/templates/templates.html
def add_renderer_globals(event):
    event['helpers'] = helpers
    event['json'] = json
    settings = pyramid.threadlocal.get_current_registry().settings
    event['site_name'] = settings.get('site_name')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    passwords_config_path = helpers.get_passwords_config_path(global_config['__file__'])
    if os.path.isfile(passwords_config_path):
        passwords_settings = helpers.load_config(passwords_config_path)
        settings = helpers.dicts_merge(passwords_settings.get('app:main', {}), settings)

    sql_engine = engine_from_config(settings, 'sqlalchemy.')
    authentication_secret = settings.get('authentication_secret')

    if authentication_secret is None:
        raise Exception('authentication_secret must be set at [conf_type]_passwords.ini!')

    # see http://docs.pylonsproject.org/projects/pyramid//en/latest/tutorials/wiki2/authorization.html
    authn_policy = AuthTktAuthenticationPolicy(secret=authentication_secret, hashalg='sha512', callback=User.get_groups)
    authz_policy = ACLAuthorizationPolicy()
    # DBSession.configure(bind=engine)p
    Base.metadata.bind = sql_engine
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings, root_factory='pyragrid.db.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_chameleon')
    config.add_translation_dirs(
        'colander:locale',
        'deform:locale',
        'pyragrid:locale'
    )

    def translator(term):
        # return get_localizer(get_current_request()).translate(term)
        return get_current_request().localizer.translate(term)

    deform_template_dir = resource_filename('deform', 'templates/')
    zpt_renderer = deform.ZPTRendererFactory(
        [deform_template_dir],
        translator=translator
    )
    deform.Form.set_default_renderer(zpt_renderer)

    payment_systems.load_by_config(config)

    static_cache_max_age = 3600
    # TODO hacky. maybe better copy resources with gulp task?
    config.add_static_view('static/fonts/bootstrap', '../bower_components/bootstrap-sass-official/assets/fonts/bootstrap', cache_max_age=static_cache_max_age)
    config.add_static_view('static/bower_components', '../bower_components', cache_max_age=static_cache_max_age)
    # config.add_static_view('static/dist', '../static/dist', cache_max_age=static_cache_max_age)
    config.add_static_view('static', 'static', cache_max_age=static_cache_max_age)
    config.add_static_view('resources', 'resources', cache_max_age=static_cache_max_age)
    config.add_static_view('static_deform', 'deform:static')

    config.add_route('index', '/')
    config.add_route('profile_edit', '/profile/edit')
    config.add_route('vk_iframe_auth', '/vkIframeAuth')
    config.add_route('test', '/t')

    # TODO delete:
    config.add_route('add_user', '/users/add')
    config.add_route('delete_user', '/users/delete/{any_data}')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('register', '/register')
    config.add_route('register_success', '/register_success')

    config.add_route('email_check_code', '/checkEmail/{code}')

    config.add_route('article', '/article/{article_system_name}')
    config.add_route('article_revision', '/article/{article_system_name}')

    config.add_route('admin_index', '/admin')
    config.add_route('admin_test', '/test')

    config.add_route('admin_users', '/admin/users')
    config.add_route('admin_users_grid', '/admin/users/grid')
    config.add_route('admin_user_enable', '/admin/users/enable/{user_id}')
    config.add_route('admin_user_disable', '/admin/users/disable/{user_id}')
    config.add_route('admin_user_edit', '/admin/users/edit/{user_id}')

    config.add_route('admin_article_edit', '/admin/article/{article_id}/edit')
    config.add_route('admin_article_enable', '/admin/article/{article_id}/enable')
    config.add_route('admin_article_disable', '/admin/article/{article_id}/disable')
    config.add_route('admin_article_revisions', '/admin/article/{article_id}/revisions')
    config.add_route('admin_article_revision', '/admin/article/{article_id}/revision/{article_revision_id}')
    config.add_route('admin_article_revision_activate', '/admin/article/{article_id}/revision/{article_revision_id}/activate')
    config.add_route('admin_article_new', '/admin/new/article')
    config.add_route('admin_articles', '/admin/articles')
    config.add_route('admin_articles_grid', '/admin/articles/grid')
    config.add_route('admin_article_revisions_grid', '/admin/article/{article_id}/revisions/grid')

    config.add_route('admin_goods', '/admin/goods')
    config.add_route('admin_goods_grid', '/admin/goods/grid')
    config.add_route('admin_good_new', '/admin/new/good')
    config.add_route('admin_good_edit', '/admin/good/{id}/edit')
    config.add_route('admin_good_enable', '/admin/good/{id}/enable')
    config.add_route('admin_good_disable', '/admin/good/{id}/disable')

    config.add_route('test_mail', '/test/mail')
    config.add_route('test_render', '/test/render')
    config.add_route('test_notify', '/test/notify')
    config.add_route('test_view_notify', '/test/view_notify')
    config.add_route('test_url', '/test/url')
    config.add_route('test_ajax', '/test/ajax')
    config.add_route('test_redirect', '/test/redirect')
    config.add_route('test_bootgrid_edit', '/test/bootgrid')
    config.add_route('test_script_inclusion', '/test/script_inclusion')
    config.add_route('test_db_enum', '/test/db_enum')
    config.add_route('test_filetree', '/test/filetree')
    config.add_route('test_ajax_filetree', '/test/ajax_filetree')
    config.add_route('test_filedialog', '/test/filedialog')
    config.add_route('test_droparea', '/test/droparea')
    config.add_route('test_jquery_file_upload', '/test/jquery_file_upload')
    config.add_route('test_blocks', '/test/blocks')
    config.add_route('test_nunjucks', '/test/nunjucks')
    config.add_route('test_jac', '/test/jac')
    config.add_route('test_mobx', '/test/mobx')
    config.add_route('test_mobx_fetch', '/test/mobx_fetch')

            # urlList: '/uploads/list'
            # urlInfo: '/uploads/info'
            # urlOperations: '/uploads/manage'

    config.add_route('uploads_list', '/uploads/list')
    config.add_route('uploads_info', '/uploads/info')
    config.add_route('uploads_manage', '/uploads/manage')
    config.add_route('uploads_handle_droparea', '/uploads/handleDropArea')
    config.add_route('uploads_handle_jquery_file_upload', '/uploads/handleJqueryFileUpload')

    config.add_route('order_status', '/order/{id}/status')

    config.add_route('good_one_click_buy', '/goods/{id}/one_click_buy')

    config.add_notfound_view(views_articles.view_custom_not_found, append_slash=True)

    config.set_session_factory(session_factory)

    config.add_subscriber(add_renderer_globals, pyramid.events.BeforeRender)

    # config.registry['mailer'] = Mailer.from_settings(settings)

    # fix vk init:
    if pyramid.threadlocal.get_current_registry().settings is None:
        pyramid.threadlocal.get_current_registry().settings = settings

    config.scan(ignore=['pyragrid.payment_systems'])
    # TODO ???????????? ?????????????????? jinja2 env ?? ????????????

    app = config.make_wsgi_app()
    jinja2_env = pyramid_jinja2.get_jinja2_environment(config)
    jac_output_dir_path = os.path.join(os.path.dirname(__file__), 'static', 'dist')
    #jinja2_env.compressor_output_dir = './pyragrid/static/dist'
    jinja2_env.compressor_output_dir = jac_output_dir_path
    jinja2_env.compressor_debug = True

    # BabelCompressor.binary = './node_modules/.bin/babel'
    BabelCompressor.binary = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'node_modules', '.bin', 'babel'))
    BabelCompressor.cwd_for_presets_search = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    BabelCompressor.presets = ['es2015', 'stage-0', 'react', 'es2016', 'es2017']
    # wtf? adds lines like `require("babel-runtime/core-js/object/get-prototype-of")` to the code
    # TODO https://babeljs.io/docs/plugins/transform-runtime/
    # BabelCompressor.plugins = ['transform-runtime']

    jac_default_config = JacDefaultConfig()
    jinja2_env.compressor_classes = jac_default_config.get('compressor_classes')
    jinja2_env.compressor_classes['text/babel'] = BabelCompressor

    return app

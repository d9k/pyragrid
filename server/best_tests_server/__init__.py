from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import (
    DBSession,
    Base,
    User
)

# from best_tests_server.models import RootFactory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    sql_engine = engine_from_config(settings, 'sqlalchemy.')
    # TODO callback= http://pyramid.chromaticleaves.com/simpleauth/
    # TODO http://docs.pylonsproject.org/projects/pyramid//en/latest/tutorials/wiki2/authorization.html
    authn_policy = AuthTktAuthenticationPolicy(secret='43ser0sroova', hashalg='sha512', callback=User.get_groups)
    authz_policy = ACLAuthorizationPolicy()
    # DBSession.configure(bind=engine)
    Base.metadata.bind = sql_engine
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings, root_factory='best_tests_server.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_chameleon')
    static_cache_max_age = 3600
    # TODO hacky. maybe better copy resources with gulp task?
    config.add_static_view('static/fonts/bootstrap', '../bower_components/bootstrap-sass-official/assets/fonts/bootstrap', cache_max_age=static_cache_max_age)
    config.add_static_view('static/bower_components', '../bower_components', cache_max_age=static_cache_max_age)
    config.add_static_view('static', 'static', cache_max_age=static_cache_max_age)
    config.add_static_view('resources', 'resources', cache_max_age=static_cache_max_age)
    config.add_static_view('static_deform', 'deform:static')
    config.add_route('home', '/')
    config.add_route('test', '/t')
    config.add_route('add_user', '/users/add')
    config.add_route('delete_user', '/users/delete/{vk_id}')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout}')
    config.set_session_factory(session_factory)
    config.scan()
    return config.make_wsgi_app()

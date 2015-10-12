from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)
from pyramid.security import has_permission
# from pyramid.url import route_url
from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User
)

from colanderalchemy import SQLAlchemySchemaNode

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)

import deform
import colander
from colander import SchemaNode
from deform import Form, Button

import pyramid.security as security

import transaction
import dictalchemy.utils
import best_tests_server.helpers as helpers

from .base_views import BaseViews


@view_defaults(route_name='index', permission='view')
class SiteViews(BaseViews):

    # def __init__(self, request):
    #     super.__init__(request)

    @view_config(route_name='index', renderer='templates/index.jinja2')
    def index_view(self):
        return {'username': self.user.name}

    @view_config(route_name='profile_edit', renderer='templates/profile_edit.jinja2')
    def profile_edit_view(self):
        return {'rendered_profile_edit_form': ''}





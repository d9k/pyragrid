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
    Article
)

from colanderalchemy import SQLAlchemySchemaNode

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)

from pyramid.request import Request

import deform
from deform import Form, Button

import transaction
import dictalchemy.utils
from pyragrid import helpers

from .forms import (
    ProfileEditSchema
)

from .views_base import (ViewsBase, conn_err_msg)
from .views_articles import ViewsArticles

@view_defaults(route_name='index', permission='view')
class ViewsSite(ViewsBase):

    # def __init__(self, request):
    #     super.__init__(request)

    @view_config(route_name='index', permission=None, renderer='templates/index.jinja2')
    def index_view(self):
        if self.user is not None:
            return {}
        article = Article.by_system_name('index')
        if article is not None:
            # views_articles = ViewsArticles(self.request)
            # return views_articles.view_article()
            article_route_url = self.request.route_url('article', article_system_name='index')
            subreq = Request.blank(article_route_url)
            response = self.request.invoke_subrequest(subreq, use_tweens=True)
            return response
        else:
            return HTTPFound('/login')

    @view_config(route_name='profile_edit', renderer='templates/profile_edit.jinja2')
    def profile_edit_view(self):
        schema = ProfileEditSchema()
        profile_edit_form = Form(
            schema.bind(),
            buttons=[Button(name='profile_edit_form_submit', title='Изменить')],
        )
        if 'profile_edit_form_submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                data = profile_edit_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(rendered_profile_edit_form=e.render())

            name = data.get('name')
            if name:
                self.user.name = name

            try:
                with transaction.manager:
                    DBSession.add(self.user)
            except DBAPIError:
                return Response(conn_err_msg, content_type='text/plain', status_int=500)

        #TODO name validator
        appstruct = dictalchemy.utils.asdict(self.user, include=['name'])
        return dict(rendered_profile_edit_form=profile_edit_form.render(appstruct))
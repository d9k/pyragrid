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
    Base,
    DBSession,
    User,
    Article,
    ArticleRevision
)

from colanderalchemy import SQLAlchemySchemaNode

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)

import deform
from deform import Form, Button

import transaction
import dictalchemy.utils
from pyragrid import helpers

from .forms import (
    ProfileEditSchema
)

from .views_base import (
    ViewsBase, conn_err_msg
)


@view_defaults(route_name='index')
class ViewsSite(ViewsBase):

    @view_config(route_name='article', renderer='templates/article.jinja2')
    def view_article(self):
        system_name = self.request.matchdict.get('article_system_name')
        if system_name is None:
            return HTTPNotFound('Название статьи не указано')

        article = Article.by_system_name(system_name)

        if article is None:
            return HTTPNotFound('Статья не найдена')

        article_revision = None

        if article.activeRevisionId is not None:
            article_revision = ArticleRevision.by_id(article.activeRevisionId)

        # schema = ProfileEditSchema()
        # profile_edit_form = Form(
        #     schema.bind(),
        #     buttons=[Button(name='profile_edit_form_submit', title='Изменить')],
        # )
        # if 'profile_edit_form_submit' in self.request.params:
        #     controls = self.request.POST.items()
        #     try:
        #         data = profile_edit_form.validate(controls)
        #     except deform.ValidationFailure as e:
        #         return dict(rendered_profile_edit_form=e.render())
        #
        #     name = data.get('name')
        #     if name:
        #         self.user.name = name
        #
        #     try:
        #         with transaction.manager:
        #             DBSession.add(self.user)
        #     except DBAPIError:
        #         return Response(conn_err_msg, content_type='text/plain', status_int=500)
        #
        # #TODO name validator
        # appstruct = dictalchemy.utils.asdict(self.user, include=['name'])
        # return dict(rendered_profile_edit_form=profile_edit_form.render(appstruct))
        return dict(article=None, article_revision=article_revision)
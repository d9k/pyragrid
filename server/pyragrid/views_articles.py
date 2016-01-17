from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config,
    notfound_view_config
)
from pyramid.security import has_permission
# from pyramid.url import route_url
from sqlalchemy.exc import DBAPIError

from .db import (
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
class ViewsArticles(ViewsBase):

    @view_config(route_name='article', renderer='templates/article.jinja2')
    def view_article(self):

        if self.notfound:
            path = self.request.path
            article = Article.by_path(path)
            if article is None:
                return HTTPNotFound('Страница не найдена')
        else:
            system_name = self.request.matchdict.get('article_system_name')
            if system_name is None:
                return HTTPNotFound('Название статьи не указано')

            article = Article.by_system_name(system_name)

            if article is None:
                return HTTPNotFound('Статья не найдена')

        self.request.override_renderer = 'templates/article.jinja2'

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
        return dict(article=article, article_revision=article_revision)


def view_custom_not_found(request):
    views_articles = ViewsArticles(request)
    return views_articles.view_article()

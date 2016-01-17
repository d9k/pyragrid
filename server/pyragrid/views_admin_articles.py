from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from .db import (
    DBSession,
    User,
    Article,
    ArticleRevision,
    db_save_model
)

from .views_base import (
    ViewsBase, conn_err_msg
)

from .views_admin import ViewsAdmin

from pyramid_mailer.mailer import Mailer
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

import transaction

from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound
)

from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc

from pyragrid import helpers, forms

from datatables import ColumnDT, DataTables

import deform

import dictalchemy.utils

from . import widgets
from .datatables_mod import DataTablesMod


class ViewsAdminArticles(ViewsAdmin):
    def __init__(self, request):
        super().__init__(request)
        self.article = None

    @view_config(route_name='admin_articles', renderer='templates/admin/admin_articles.jinja2')
    def view_admin_articles(self):
        return {}

    @view_config(route_name='admin_articles_grid', request_method='GET', renderer='json')
    def view_admin_articles_grid(self):
        columns = [
            ColumnDT('id'),
            ColumnDT('name'),
            ColumnDT('systemName'),
            ColumnDT('path'),
            ColumnDT('activeRevisionId'),
            ColumnDT('active'),
        ]
        query = DBSession.query(Article)
        # instantiating a DataTable for the query and table needed
        row_table = DataTablesMod(self.request.GET, Article, query, columns)

        # returns what is needed by DataTable
        result = row_table.output_result()
        result = helpers.datatables_result_add_fake_column(result)
        return result

    @view_config(route_name='admin_article_edit', renderer='templates/admin/admin_article_edit.jinja2')
    @view_config(route_name='admin_article_new', renderer='templates/admin/admin_article_edit.jinja2')
    def view_admin_article_edit(self):
        article_id = self.request.matchdict.get('article_id')
        article_is_new = self.request.matched_route.name == 'admin_article_new'
        if article_id is not None:
            article = Article.by_id(article_id)
        else:
            if article_is_new:
                article = Article()
            else:
                return HTTPBadRequest('No article id specified')

        if not article:
            return HTTPNotFound('Article not found')

        self.article = article
        current_revision = None
        if article.activeRevisionId is not None:
            current_revision = ArticleRevision.by_id(article.activeRevisionId)

        # if 'article_delete' in self.request.params:
        #     try:
        #         with transaction.manager:
        #             DBSession.delete(article)
        #     except DBAPIError:
        #         return Response(conn_err_msg, content_type='text/plain', status_int=500)
        #     return HTTPFound(self.request.route_url('admin_articles'))

        article_edit_schema = forms.ArticleEditSchema()
        article_edit_schema.linked_article = article

        article_edit_form = widgets.FormEx(
            article_edit_schema.bind(),
            formid='articleEdit',
            buttons=[widgets.ButtonEx(
                    name='form_article_edit_submit',
                    title='Создать' if article_is_new else 'Изменить'
            )],
        )

        if 'form_article_edit_submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                data = article_edit_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(rendered_form=e.render())

            # TODO proper binding
            # user.name = data.get('name')
            # user.vk_id = data.get('vk_id')

            helpers.obj_set_fields_from_dict(article, data)

            new_code = data.get('code')
            if new_code:
                # TODO load revision, compare code, if changed, then create revision
                save_revision = True
                parent_revision_id = None
                if current_revision is not None:
                    if current_revision.code == new_code:
                        save_revision = False
                    parent_revision_id = current_revision.id
                if save_revision:
                    new_revision = ArticleRevision()

                    if article_id is None:
                        error = db_save_model(article)
                        if error is not None:
                            return self.db_error_response(error)

                    new_revision.articleId = article.id
                    new_revision.authorId = self.user.id
                    new_revision.code = new_code
                    new_revision.parentRevisionId = parent_revision_id

                    error = db_save_model(new_revision)
                    if error is not None:
                        return self.db_error_response(error)

                    article.activeRevisionId = new_revision.id
                    current_revision = new_revision

            # raise Exception('not implemented yet')

            error = db_save_model(article)
            if error is not None:
                return self.db_error_response(error)

            self.add_success_flash('Статья успешно изменена')

            if article_is_new:
                return HTTPFound(self.request.route_url('admin_article_edit', article_id=article.id))

        appstruct = dictalchemy.utils.asdict(article)
        if current_revision is not None:
            appstruct['code'] = current_revision.code

        # TODO name validator
        appstruct = helpers.dict_set_empty_string_on_null(appstruct)

        # TODO fix vk_id
        # appstruct['vk_id'] = 0
        return dict(rendered_form=article_edit_form.render(appstruct))

    @view_config(route_name='admin_article_enable', renderer='json')
    def view_admin_article_enable(self):
        article_id = self.request.matchdict.get('article_id')
        if not article_id:
            return HTTPBadRequest('No article id specified')
        article = Article.by_id(article_id)
        if not article:
            return HTTPNotFound('Article not found')
        article.active = True

        error = db_save_model(article)
        if error is not None:
            return self.db_error_response(error)

        return {'result': 'success', 'message': 'Статья актирована'}

    @view_config(route_name='admin_article_disable', renderer='json')
    def view_admin_article_disable(self):
        article_id = self.request.matchdict.get('article_id')
        if not article_id:
            return HTTPBadRequest('No article id specified')
        article = Article.by_id(article_id)
        if not article:
            return HTTPNotFound('Article not found')
        article.active = False

        error = db_save_model(article)
        if error is not None:
            return self.db_error_response(error)

        return {'result': 'success', 'message': 'Статья отключена'}

    @view_config(route_name='admin_article_revision', renderer='templates/admin/admin_article_revisions.jinja2')
    @view_config(route_name='admin_article_revisions', renderer='templates/admin/admin_article_revisions.jinja2')
    def view_admin_article_revision(self):
        article_id = self.request.matchdict.get('article_id')
        if article_id is not None:
            article = Article.by_id(article_id)
        else:
            return HTTPBadRequest('No article id specified')

        if article is None:
            return HTTPNotFound('Article not found')

        article_revision_id = self.request.matchdict.get('article_revision_id')

        if article_revision_id is None:
            article_revision_id = article.activeRevisionId
        selected_revision = ArticleRevision.by_id(article_revision_id, article_id)

        return dict(article=article, selected_revision=selected_revision)

    @view_config(route_name='admin_article_revisions_grid', request_method='GET', renderer='json')
    def view_admin_article_revisions_grid(self):
        columns = [
            ColumnDT('id'),
            ColumnDT('article.systemName'),
            ColumnDT('parentRevisionId'),
            ColumnDT('dateTime'),
            ColumnDT('author.login'),
        ]
        article_id = self.request.matchdict.get('article_id')
        query = DBSession.query(ArticleRevision)\
            .join(Article)\
            .join(User)\
            .filter(ArticleRevision.articleId == article_id)\
            .order_by(desc(ArticleRevision.dateTime))
        # instantiating a DataTable for the query and table needed
        row_table = DataTablesMod(self.request.GET, ArticleRevision, query, columns)

        # returns what is needed by DataTable
        result = row_table.output_result()
        result = helpers.datatables_result_add_fake_column(result)
        return result

    @view_config(route_name='admin_article_revision_activate', renderer='json')
    def view_admin_article_revision_activate(self):
        article_id = self.request.matchdict.get('article_id')

        if article_id is not None:
            article = Article.by_id(article_id)
        else:
            return HTTPBadRequest('Id статьи не указан')

        if article is None:
            return HTTPNotFound('Статья не найдена')

        article_revision_id = self.request.matchdict.get('article_revision_id')
        if article_revision_id is None:
            return HTTPNotFound('Id ревизии не указан')

        selected_revision = ArticleRevision.by_id(article_revision_id, article_id)
        if selected_revision is None:
            return HTTPNotFound('Ревизия статьи не найдена')

        article.activeRevisionId = selected_revision.id

        error = db_save_model(article)
        if error is not None:
            return self.db_error_response(error)

        return {'result': 'success', 'message': 'Ревизия установлена'}


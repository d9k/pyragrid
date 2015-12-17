from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from .models import (
    DBSession,
    User,
    Article
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

from pyragrid import helpers, forms

from datatables import ColumnDT, DataTables

import deform

import dictalchemy.utils

from . import widgets
from .datatables_mod import DataTablesMod


class ViewsAdminArticles(ViewsAdmin):
    @view_config(route_name='admin_articles', renderer='templates/admin/admin_articles.jinja2')
    def admin_articles_view(self):
        return {}

    @view_config(route_name='admin_articles_grid', request_method='GET', renderer='json')
    def admin_articles_grid_view(self):
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
        article_id = self.request.GET.get('article_id')
        if article_id is not None:
            article = Article.by_id(article_id)
        else:
            if self.request.matched_route.name == 'admin_article_new':
                article = Article()
            else:
                return HTTPBadRequest('No article id specified')

        if not article:
            return HTTPNotFound('Article not found')

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
            buttons=[widgets.ButtonEx(name='form_article_edit_submit', title='Изменить')],
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
            revision_code = data.get('code')
            if revision_code:
                # TODO load revision, compare code, if changed, then create revision
                pass

            # raise Exception('not implemented yet')

            try:
                with transaction.manager:
                    DBSession.add(article)
            except DBAPIError:
                return Response(conn_err_msg, content_type='text/plain', status_int=500)

            self.add_success_flash('Статья успешно изменена')

        # TODO name validator
        appstruct = helpers.dict_set_empty_string_on_null(dictalchemy.utils.asdict(article))
        # TODO fix vk_id
        # appstruct['vk_id'] = 0
        return dict(rendered_form=article_edit_form.render(appstruct))

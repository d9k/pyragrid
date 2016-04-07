from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from .db import (
    DBSession,
    Good,
    User
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


class ViewsAdminGoods(ViewsAdmin):
    def __init__(self, request):
        super().__init__(request)
        self.good = None

    @view_config(route_name='admin_goods', renderer='templates/admin/admin_goods.jinja2')
    def view_admin_goods_view(self):
        return {}

    @view_config(route_name='admin_goods_grid', request_method='GET', renderer='json')
    def view_admin_goods_grid_view(self):
        columns = [
            ColumnDT('id'),
            ColumnDT('name'),
            ColumnDT('isEgood'),
            ColumnDT('price'),
            ColumnDT('active'),
        ]
        query = DBSession.query(Good)
        # instantiating a DataTable for the query and table needed
        row_table = DataTablesMod(self.request.GET, Good, query, columns)

        # returns what is needed by DataTable
        result = row_table.output_result()
        result = helpers.datatables_result_add_fake_column(result)
        return result

    @view_config(route_name='admin_good_enable', renderer='json')
    def view_admin_good_enable(self):
        good_id = self.request.matchdict.get('id')
        if not good_id:
            return HTTPBadRequest('No good id specified')
        good = Good.by_id(good_id)
        if not good:
            return HTTPNotFound('Good not found')
        good.active = True
        with transaction.manager:
            DBSession.add(good)
        return {'result': 'success', 'message': 'Товар актирован'}

    @view_config(route_name='admin_good_disable', renderer='json')
    def view_admin_good_disable(self):
        id = self.request.matchdict.get('id')
        if not id:
            return HTTPBadRequest('No good id specified')
        good = Good.by_id(id)
        if not good:
            return HTTPNotFound('Good not found')
        good.active = False
        with transaction.manager:
            DBSession.add(good)
        return {'result': 'success', 'message': 'Товар отключен'}

    @view_config(route_name='admin_good_new', renderer='templates/admin/admin_good_edit.jinja2')
    @view_config(route_name='admin_good_edit', renderer='templates/admin/admin_good_edit.jinja2')
    def view_admin_good_edit(self):
        id = self.request.matchdict.get('id')
        is_new = self.request.matched_route.name == 'admin_good_new'

        if is_new:
            self.good = Good()
        else:
            if not id:
                return HTTPBadRequest('No good id specified')
            self.good = Good.by_id(id)
            if not self.good:
                return HTTPNotFound('Good not found')

        if 'good_delete' in self.request.params:
            try:
                with transaction.manager:
                    DBSession.delete(self.good)
            except DBAPIError:
                return Response(conn_err_msg, content_type='text/plain', status_int=500)
            return HTTPFound(self.request.route_url('admin_goods'))

        good_edit_schema = forms.GoodEditSchema()
        good_edit_schema.linked_good = self.good

        submit_button_title = 'Создать' if is_new else 'Изменить'

        good_edit_form = widgets.FormMod(
            good_edit_schema.bind(),
            buttons=[widgets.ButtonMod(name='good_edit_form_submit', title=submit_button_title),
                     # widgets.ButtonEx(name='good_delete', title='X', css_class='btn-danger',
                     #                  description="Удалить пользователя")
                     ],
        )

        if 'good_edit_form_submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                data = good_edit_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(rendered_form=e.render())

            # # TODO proper binding
            # # user.name = data.get('name')
            # # user.vk_id = data.get('vk_id')

            helpers.obj_set_fields_from_dict(self.good, data)
            # password = data.get('password')
            # if password:
            #     good.set_password(password)

            try:
                with transaction.manager:
                    DBSession.add(self.good)
            except DBAPIError:
                return Response(conn_err_msg, content_type='text/plain', status_int=500)

            self.add_success_flash('Товар успешно изменён')

        appstruct = dictalchemy.utils.asdict(self.good)
        appstruct = helpers.dict_set_empty_string_on_null(appstruct)

        return dict(rendered_form=good_edit_form.render(appstruct))

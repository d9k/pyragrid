from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from .models import (
    DBSession,
    User
)

from .base_views import (
    BaseViews, conn_err_msg
)

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


@view_defaults(permission='admin')
class AdminViews(BaseViews):

    @view_config(route_name='admin_index', renderer='templates/admin/admin_index.jinja2')
    def admin_index_view(self):
        return {'username': self.user.name}

    @view_config(route_name='admin_users', renderer='templates/admin/admin_users.jinja2')
    def admin_users_view(self):
        return {'username': self.user.name}

    @view_config(route_name='admin_users_grid', request_method='GET', renderer='json')
    def admin_users_grid_view(self):
        columns = [
            ColumnDT('id'),
            ColumnDT('vk_id'),
            ColumnDT('login'),
            ColumnDT('name'),
            ColumnDT('email'),
            ColumnDT('email_checked'),
            ColumnDT('active')
        ]
        query = DBSession.query(User)
        # instantiating a DataTable for the query and table needed
        row_table = DataTablesMod(self.request.GET, User, query, columns)

        # returns what is needed by DataTable
        result = row_table.output_result()
        result = helpers.datatables_result_add_fake_column(result)
        return result

    # @view_config(route_name='admin_user_disable')
    # def admin_user_disable_view(self):

    @view_config(route_name='delete_user', renderer='templates/default_page.jinja2')
    def delete_user_view(self):

        try:
            with transaction.manager:
                any_data = self.request.matchdict.get('any_data')
                id_ = self.request.matchdict.get('id')
                """:type : User"""
                user = None
                if any_data:
                    # DBSession.query(User).filter(User.vk_id == vk_id).delete()
                    user = User.by_any(any_data)
                elif id_:
                    user = User.by_id(id_)
                else:
                    return HTTPBadRequest('can\'t find user: no data specified')

                if not user:
                    return HTTPBadRequest('can\'t find user')
                DBSession.delete(user)
                # transaction.commit()

        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)
        return {'content': 'user ' + user.name + ' deleted'}

    @view_config(route_name='admin_user_enable', renderer='json')
    def admin_user_enable(self):
        user_id = self.request.matchdict.get('user_id')
        if not user_id:
            return HTTPBadRequest('No user id specified')
        user = User.by_id(user_id)
        if not user:
            return HTTPNotFound('User not found')
        user.active = True
        with transaction.manager:
            DBSession.add(user)
        return {'result': 'success', 'message': 'Пользователь актирован'}

    @view_config(route_name='admin_user_disable', renderer='json')
    def admin_user_disable(self):
        user_id = self.request.matchdict.get('user_id')
        if not user_id:
            return HTTPBadRequest('No user id specified')
        user = User.by_id(user_id)
        if not user:
            return HTTPNotFound('User not found')
        user.active = False
        with transaction.manager:
            DBSession.add(user)
        return {'result': 'success', 'message': 'Пользователь отключен'}

    @view_config(route_name='admin_user_edit', renderer='templates/admin/admin_user_edit.jinja2')
    def admin_user_edit(self):
        user_id = self.request.matchdict.get('user_id')
        if not user_id:
            return HTTPBadRequest('No user id specified')
        user = User.by_id(user_id)
        if not user:
            return HTTPNotFound('User not found')

        if 'user_delete' in self.request.params:
            try:
                with transaction.manager:
                    DBSession.delete(user)
            except DBAPIError:
                return Response(conn_err_msg, content_type='text/plain', status_int=500)
            return HTTPFound(self.request.route_url('admin_users'))

        user_edit_schema = forms.UserEditSchema()
        user_edit_schema.linked_user = user

        user_edit_form = widgets.FormEx(
            user_edit_schema.bind(),
            buttons=[widgets.ButtonEx(name='user_edit_form_submit', title='Изменить'),
                     widgets.ButtonEx(name='user_delete', title='X', css_class='btn-danger',
                                      description="Удалить пользователя")],
        )

        if 'user_edit_form_submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                data = user_edit_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(rendered_form=e.render())

            # TODO proper binding
            # user.name = data.get('name')
            # user.vk_id = data.get('vk_id')

            helpers.obj_fields_from_dict(user, data)
            password = data.get('password')
            if password:
                user.set_password(password)

            try:
                with transaction.manager:
                    DBSession.add(user)
            except DBAPIError:
                return Response(conn_err_msg, content_type='text/plain', status_int=500)

            self.add_success_flash('Пользователь успешно изменён')

        # TODO name validator
        appstruct = dictalchemy.utils.asdict(user)
        # TODO fix vk_id
        # appstruct['vk_id'] = 0
        return dict(rendered_form=user_edit_form.render(appstruct))

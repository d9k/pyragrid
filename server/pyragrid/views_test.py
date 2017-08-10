from pyramid.response import Response
from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config
)

from enum import Enum

from .db import (
    DBSession,
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

from pyragrid import helpers

from datatables import ColumnDT, DataTables


class Testiews(ViewsAdmin):
    @view_config(route_name='test_mail', renderer='templates/test/test_base.jinja2')
    def view_test_mail_view(self):
        # try:
        # with transaction.manager:
        """ :type : Mailer """
        # mailer = self.request.registry['mailer']
        mailer = get_mailer(self.request)
        message = Message(subject="test pyramid email send",
                          sender="d9kd9k@gmail.com",
                          recipients=['d9k@ya.ru'],
                          body="test body")
        mailer.send(message)
        transaction.commit()
        # except:
        #     return {'content': 'Error on email sending'}
        # TODO test headers from view name
        return {'header': 'Test Email', 'content': 'Email sent (?)'}

    @view_config(route_name='test_render', renderer='templates/test/test_base.jinja2')
    def view_test_render_view(self):
        rendered_view = helpers.render_to_string('templates/test_render/test_render.jinja2', self.request, {})
        return {'header': 'Test Render', 'code_block': rendered_view}

    @view_config(route_name='test_notify', renderer='templates/test/test_notify.jinja2')
    def view_test_notify(self):
        return {'header': 'Test notify'}

    @view_config(route_name='test_view_notify', renderer='templates/test/test_base.jinja2')
    def view_test_view_notify(self):
        self.add_success_flash('Тестирование успеха')
        self.add_error_flash('Тестирование ошибки')
        self.add_success_flash('И снова успех!')
        return {'header': 'Test view notify'}

    @view_config(route_name='test_url', renderer='templates/test/test_url.jinja2')
    def view_test_url(self):
        return {'header': 'Test url'}

    @view_config(route_name='test_ajax', renderer='templates/test/test_ajax.jinja2')
    def view_test_ajax(self):
        if self.request.method == 'GET':
            counter = int(self.request.GET.get('counter', 0))
        else:
            counter = int(self.request.POST.get('counter', 0))
        counter += 1
        return dict(header='Test ajax', counter=counter)

    @view_config(route_name='test_redirect', renderer='templates/test/test_base.jinja2')
    def view_test_redirect(self):
        admin_url = self.request.route_url('admin_index')
        return HTTPFound(location=admin_url)

    @view_config(route_name='test_bootgrid_edit', renderer='templates/test/test_bootgrid_edit.jinja2')
    def view_test_bootgrid_edit(self):
        return dict(header='Test bootstrap grid editor')

    @view_config(route_name='test_script_inclusion', renderer='templates/test/test_base.jinja2')
    def view_test_script_inclusion(self):
        import pyragrid.scripts.parse_config as parse_config
        # ini_path = parse_config.get_ini_path('development')
        settings = parse_config.load_merged_ini('development')
        db_connection_url = parse_config.get_connection_url_from_settings(settings)
        db_connection_params = parse_config.db_connection_params_from_url(db_connection_url)
        return dict(header='Test script inclusion', content='db name is '+parse_config.quote(db_connection_params['name']))

    @view_config(route_name='test_db_enum', renderer='templates/test/test_base.jinja2')
    def view_test_db_enum(self):
        # see http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/

        from pyragrid.db import (DeclEnum, SimpleEnum)

        # class EmployeeType(DeclEnum):
        #     part_time = "P", "Part Time"
        #     full_time = "F", "Full Time"
        #     contractor = "C", "Contractor"
        #
        # vals = EmployeeType.values()

        class EmployeeTypeEnum(SimpleEnum):
            part_time = '', 'Part time'
            full_time = ''
            contractor = ''

        import sqlalchemy
        from sqlalchemy import Column
        from .db import Base

        values = EmployeeTypeEnum.get_values()

        # EmployeeTypeEnum = Enum('a', 'za', 'zaa')

        enumDeclaration = sqlalchemy.Enum(*EmployeeTypeEnum.get_values())
        nativeEnumDeclaration = sqlalchemy.Enum(*EmployeeTypeEnum.get_values(), native_enum=True)

        class TestModel(Base):
            __tablename__ = 'testModels'

            id = Column(sqlalchemy.Integer, primary_key=True,)
            enum_test = Column(sqlalchemy.Enum(*EmployeeTypeEnum.get_values(), native_enum=True))

        return {'header': 'Test DB Enum', 'content': 'use debugger to see'}

    @view_config(route_name='test_filetree', renderer='templates/test/test_filetree.jinja2')
    def view_test_filetree(self):

        return {'header': 'Jqueryfiletree test'}

    @view_config(route_name='test_droparea', renderer='templates/test/test_droparea.jinja2')
    def view_test_droparea(self):

        return {'header': 'jquery droparea test'}

    @view_config(route_name='test_jquery_file_upload', renderer='templates/test/test_jquery_file_upload.jinja2')
    def view_test_jquery_file_upload(self):
        return {'header': 'jquery file upload test'}

    # thx 2 http://stackoverflow.com/a/9333816
    @staticmethod
    def toBool(val):
        if str(val).lower() in ('yes', 'y', 'true',  't', '1'):
            return True
        if str(val).lower() in ('no',  'n', 'false', 'f', '0', '0.0', '', 'none', '[]', '{}'):
            return False
        raise Exception('Invalid value for boolean conversion: ' + str(val))

    @view_config(route_name='test_ajax_filetree', renderer='string')
    def view_ajax_filetree(self):
        request = self.request

        only_folders = self.toBool(request.POST.get('onlyFolders', False))
        only_files = self.toBool(request.POST.get('onlyFiles', False))
        show_files = not only_folders
        show_folders = not only_files
        if not show_files and not show_folders:
            show_files = True

        import os

        r = ['<ul class="jqueryFileTree" style="display: none;">']
        try:
            server_path = helpers.get_server_path()

            uploads_path = os.path.join(server_path, 'uploads')

            dir_ = request.POST.get('dir', '')
            dir_ = dir_.strip(' /\\')

            dir_path = os.path.join(uploads_path, dir_)

            if os.path.isdir(dir_path):
                # TODO d = server_dir_path + d
                for node_name in os.listdir(dir_path):
                    node_path = os.path.join(dir_path, node_name)
                    node_rel_path = '/' + os.path.relpath(node_path, uploads_path)
                    if os.path.isdir(node_path):
                        if show_folders:
                            r.append('<li class="directory collapsed"><a rel="%s/">%s</a></li>' % (node_rel_path, node_name))
                    else:
                        if show_files:
                            ext = os.path.splitext(node_name)[1][1:]  # get .ext and remove dot
                            r.append('<li class="file ext_%s"><a rel="%s">%s</a></li>' % (ext, node_rel_path, node_name))

        except Exception as exc:
            r.append('Could not load directory: %s' % str(exc))
        r.append('</ul>')
        return ''.join(r)

    @view_config(route_name='test_filedialog', renderer='templates/test/test_filedialog.jinja2')
    def view_test_filetree(self):
        return {'header': 'JqueryFileDialog test'}

    @view_config(route_name='test_blocks', renderer='templates/test/test_blocks.jinja2')
    def view_test_blocks(self):
        return {
            'header': 'blocks test',
            'content_raw': '{{ render_block("hello_world") }}'
        }

from .views_admin import ViewsAdmin
from pyramid.view import (
    view_config,
)
from . import helpers


class ViewsUploads(ViewsAdmin):
    @view_config(route_name='uploads_list', renderer='string')
    def view_uploads_list(self):
        request = self.request

        only_folders = helpers.to_bool(request.POST.get('onlyFolders', False))
        only_files = helpers.to_bool(request.POST.get('onlyFiles', False))
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

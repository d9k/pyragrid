from .views_admin import ViewsAdmin
from pyramid.view import (
    view_config,
)
from . import helpers
import os
import os.path
from pyramid.response import Response
import urllib.parse
import shutil


def get_uploads_path():
    server_path = helpers.get_server_path()
    return os.path.join(server_path, 'uploads')


def get_abs_path(request_subfolder):
    uploads_path = get_uploads_path()
    request_subfolder = request_subfolder.strip(' /\\')
    return os.path.join(uploads_path, request_subfolder)


def file_size_format(bytes, suffix='B'):
    # for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(bytes) < 1024.0:
            # return "%3.1f%s%s" % (bytes, unit, suffix)
            return "%d %s%s" % (bytes, unit, suffix)
        bytes /= 1024.0
    return "%d %s%s" % (bytes, 'Y', suffix)
    # return "%.1f%s%s" % (bytes, 'Yi', suffix)


def get_file_size(file):
    file.seek(0, 2)  # Seek to the end of the file
    size = file.tell()  # Get the position of EOF
    file.seek(0)  # Reset the file position to the beginning
    return size


class Continue(Exception):
    pass


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

        r = ['<ul class="jqueryFileTree" style="display: none;">']
        try:
            uploads_path = get_uploads_path()

            dir_ = request.POST.get('dir', '')
            dir_path = get_abs_path(dir_)

            if not os.path.isdir(dir_path):
                return Response(body='Error: Hey, it is not a dir!',
                                content_type='text/plain',
                                status_int=403)

            for node_name in os.listdir(dir_path):
                node_path = os.path.join(dir_path, node_name)
                node_rel_path = '/' + os.path.relpath(node_path, uploads_path)
                if node_rel_path.find('..' + os.sep) != -1:
                    return Response(body='Error: I would NOT go upper in directory tree',
                                    content_type='text/plain',
                                    status_int=403)
                if os.path.isdir(node_path):
                    if show_folders:
                        r.append(
                            '<li class="directory collapsed"><a rel="%s/">%s</a></li>' % (node_rel_path, node_name))
                else:
                    if show_files:
                        ext = os.path.splitext(node_name)[1][1:]  # get .ext and remove dot
                        r.append('<li class="file ext_%s"><a rel="%s">%s</a></li>' % (ext, node_rel_path, node_name))

        except Exception as exc:
            r.append('Could not load directory: %s' % str(exc))
        r.append('</ul>')
        return ''.join(r)

    # @view_config(route_name='uploads_info', renderer='string')
    @view_config(route_name='uploads_info', renderer='json')
    def view_uploads_info(self):
        file_rel_path = self.request.POST.get('path', '')
        file_path = get_abs_path(file_rel_path)
        file_size_bytes = os.path.getsize(file_path)
        file_size = file_size_format(file_size_bytes)
        # TODO access rights
        # TODO strip beginning /
        # return \
        #     '<p><b>path: </b>' + file_rel_path + '</p>' \
        #     '<p><b>size: </b>' + file_size + '</p>'
        return {
            'path': file_rel_path,
            'sizeInBytes': file_size_bytes
        }

    @view_config(route_name='uploads_handle_droparea', renderer='json')
    def view_handle_droparea(self):
        return Response(body='Not implemented yet',
                        content_type='text/plain',
                        status_int=500)
        # <?php
        # // LOG
        # $log = '=== ' . @date('Y-m-d H:i:s') . ' ===============================' . "\n"
        #         . 'FILES:' . print_r($_FILES, 1) . "\n"
        #         . 'POST:' . print_r($_POST, 1) . "\n";
        # $fp = fopen('upload-log.txt', 'a');
        # fwrite($fp, $log);
        # fclose($fp);
        # // Result object
        result = {}
        # $r = new stdClass();
        # // Result content type
        # header('content-type: application/json');
        # // Maximum file size
        # $maxsize = 10; //Mb

        max_size_mb = 10

        xfile = self.request.POST.get('xfile')
        if xfile is None:
            return Response(body='Error: No xfile in POST',
                            content_type='text/plain',
                            status_int=400)

        # // File size control
        # if ($_FILES['xfile']['size'] > ($maxsize * 1048576)) {
        #     $r->error = "Max file size: $maxsize Kb";
        # }
        # // Uploading folder
        # $folder = 'files/';

        uploads_path = get_uploads_path()

        file_name = xfile.filename
        input_file = xfile.file

        # if (!is_dir($folder))
        #     mkdir($folder);
        # // If specifics folder
        # $folder .= $_POST['folder'] ? $_POST['folder'] . '/' : '';
        # if (!is_dir($folder))
        #     mkdir($folder);
        # // If the file is an image
        # if (preg_match('/image/i', $_FILES['xfile']['type'])) {
        #     $filename = $_POST['value'] ? $_POST['value'] :
        #             $folder . sha1(@microtime() . '-' . $_FILES['xfile']['name']) . '.jpg';
        # } else {
        #     $tld = split(',', $_FILES['xfile']['name']);
        #     $tld = $tld[count($tld) - 1];
        #     $filename = $_POST['value'] ? $_POST['value'] :
        #             $folder . sha1(@microtime() . '-' . $_FILES['xfile']['name']) . $tld;
        # }
        # // Supporting image file types
        # $types = Array('image/png', 'image/gif', 'image/jpeg');
        # // File type control
        # if (in_array($_FILES['xfile']['type'], $types)) {
        #     // Create an unique file name
        #     // Uploaded file source
        #     $source = file_get_contents($_FILES["xfile"]["tmp_name"]);
        #     // Image resize
        #     imageresize($source, $filename, $_POST['width'], $_POST['height'], $_POST['crop'], $_POST['quality']);
        # } else
        # // If the file is not an image
        #     move_uploaded_file($_FILES["xfile"]["tmp_name"], $filename);
        # // File path
        # $path = str_replace('upload.php', '', $_SERVER['SCRIPT_NAME']);
        # // Result data
        # $r->filename = $filename;
        # $r->path = $path;
        # $r->img = '<img src="' . $path . $filename . '" alt="image" />';
        # // Return to JSON
        # echo json_encode($r);

    @view_config(route_name='uploads_handle_jquery_file_upload', renderer='json')
    def view_handle_jquery_file_upload(self):

        uploads_subfolder = self.request.GET.get('folder', '')

        post = self.request.POST
        # TODO read from settings:
        max_file_size_mb = 20

        results = []
        for name, field_storage in post.items():
            # if type(fieldStorage) is unicode:
            #     continue
            file_name = urllib.parse.unquote(field_storage.filename)
            file_size = get_file_size(field_storage.file)
            result = dict(
                name=file_name,
                type=field_storage.type,
                size=file_size
            )

            uploads_path = get_uploads_path()
            file_folder_path = get_abs_path(uploads_subfolder)
            file_path = os.path.join(file_folder_path, file_name)

            try:
                file_rel_path = '/' + os.path.relpath(file_path, uploads_path)
                if file_rel_path.find('..' + os.sep) != -1:
                    result['error'] = 'I would NOT go upper in directory tree'
                    raise Continue

                if file_size > max_file_size_mb * 1024 * 1024:
                    result['error'] = 'File is too big. Max file size is '+str(max_file_size_mb)+' mb'
                    raise Continue

                if os.path.isfile(file_path):
                    result['error'] = 'File already exists'
                    raise Continue

                temp_file_path = file_path + '~'
                input_file = field_storage.file

                with open(temp_file_path, 'wb') as temp_file:
                    shutil.copyfileobj(input_file, temp_file)

                os.rename(temp_file_path, file_path)
            except Continue:
                pass

            results.append(result)

        return {"files": results}
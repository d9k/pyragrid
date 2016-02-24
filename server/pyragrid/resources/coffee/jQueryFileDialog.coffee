(($) ->
    $.fn.fileDialog = (options) ->
        options = options | {}
        defaultOptions = {
            dialogTitle: 'File select',
            manualInput: false
            urlList: '/uploads/list'
            urlInfo: '/uploads/info'
            urlOperations: '/uploads/manage' # move, rename, delete
            urlUpload: '/uploads/upload'
# TODO           showFilesOrFolders: 'any' # 'any'|'files'|'folders'
# TODO           selectFilesOrFolders: 'file' # 'file'|'folder'|'none'
            # TODO 'file'|'files'|'folder'|'folders'|'none'
# TODO            showInfo: true
# TODO           showOperations: true
# TODO           showClear: true
# TODO           showDelete: true
# TODO           showUpload: true
            fileTreeOptions: {
                expandSpeed: 120
                collapseSpeed: 120
                multiFolder: false
            }
            # TODO translation
        }
        #TODO make from widget's `data-` attributes; class="jQueryFileDialog" runs functions automatically
        #TODO actions: openFileDialog, restoreOriginalHtml, getData
        #TODO configurable defaultOptions (dataTable ?)
        options = $.extend(true, defaultOptions, options)
        data = {
            selectedFile: ''
            selectedFolder: ''
            inputHtml: ''
            fileInfo: {
                path: ''
                size: ''
                additionalHtml: ''
            }
        }

        fileInput = this
        fileInputId = fileInput.attr('id')
        if not fileInputId
            error 'id of field is required'
            return
        buttonClearId = fileInputId+'_clear'
        replaceMeId = 'replaceMeWith_'+fileInputId
        buttonBrowseId = fileInputId+'_browse'
        inputGroupId = fileInputId+'_group'
        modalId = fileInputId+'_modal'
        fileTreeId = fileInputId+'_fileTree'

        buttonClear = fileInput.next('button#' + buttonClearId)
        if buttonClear.length
            error 'file dialog already applied to field'
            return

        # TODO http://api.jquery.com/after/ - append buttons (clear/open dialog) next to element
        # TODO input groups http://getbootstrap.com/css/#forms-control-validation
        # TODO button groups http://getbootstrap.com/components/
        fileInput.after('
            <div id="'+inputGroupId+'" class="input-group">
              <div id="'+replaceMeId+'" />
              <span class="input-group-btn">
                <button id="'+buttonClearId+'" class="btn btn-default" type="button" title="Clear value"><span class="glyphicon glyphicon-remove"></span></button>
                <button id="'+buttonBrowseId+'" class="btn btn-default" type="button" title="Browse..." data-toggle="modal" data-target="#'+modalId+'"><span class="glyphicon glyphicon-folder-open"></span></button>
              </span>
            </div>
        ')

        formatFileSize = (bytes, _1000) ->
            size = bytes
            divisor = if _1000 then 1000 else 1024
            if Math.abs(size) < divisor
                return size + ' B'
            units = if _1000
                ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
            else
                ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

            unitIndex = -1
            loop
                size /= divisor
                ++unitIndex
                if Math.abs(size) <= divisor or unitIndex > units.length - 1
                    break

            size.toFixed(1) + ' ' + units[unitIndex]

        data.inputHtml = fileInput.html();
        $('#'+fileInputId).replaceAll($('#'+replaceMeId))
        $fileInput = $('#'+fileInputId)
        $fileInput.addClass('form-control')
        $fileInput.attr('type', 'text')

        # <input id="'+id+'" class="form-control" type="text">

        $('body').prepend('
            <div class="fileDialogModal modal fade" id="'+modalId+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
              <div class="modal-dialog" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h4 class="modal-title" id="myModalLabel">'+options.dialogTitle+'</h4>
                  </div>
                  <div class="modal-body">
                    <div class="row">
                        <div class="col-md-7">
                            <div class="column">
                                <div class="fileTreeRoot" id="'+fileTreeId+'" ></div>
                            </div>
                        </div>
                        <div class="col-md-5">
                            <div class="column">
                                <h3>File info</h3>
                                <div class="fileInfo">
                                </div>
                            </div>
                            <div class="buttons">
                                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                                <button type="button" class="btn btn-primary selectFileButton">Select file</button>
                            </div>
                        </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
        ')

        $fileDialog = $('#'+modalId)
        $selectFileButton = $('.selectFileButton', $fileDialog)
        $fileInfo = $('.fileInfo', $fileInfo)

        fileTreeOptions = $.extend(true, options.fileTreeOptions, {
            root: '/'
            script: options.urlList
        })

        renderFileInfo = (data) ->
            if !data.path
                return 'Error: no data.path set'

            html = '<p><b>file path:</b> ' + data.path + '</p>'

            if data.size
                html += '<p><b>size:</b> ' + formatFileSize(data.size) + '</p>'

            return html

        $('#'+fileTreeId).fileTree(fileTreeOptions, (file) ->
            $selectFileButton.show();
#            alert(file);
            data.selectedFile = file
            $fileInfo.html(renderFileInfo({path: file}));
            $.ajax({
                type: "POST"
                url: options.urlInfo
                data: {path: file}
                success: (data) ->
                        $fileInfo.html(renderFileInfo(data));

                dataType: 'json'
            });
            return
        );

        $selectFileButton.hide();
        $selectFileButton.on 'click', () ->
            $fileInput.val(data.selectedFile);
            $fileDialog.modal('hide')

        # TODO edit-in-place file info (access rights, path)
        # TODO so server passes json file info array to client, not rendered html

        # TODO reload jQueryFileTree every dialog open and after file move
        # TODO "upload file here" button
        # TODO highlight selected folder in file tree
    ) jQuery
# make file visible on source tree when dynamically loaded
`
//# sourceURL=jQueryFileDialog.js
//`
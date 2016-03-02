(($) ->

    # file info subcomponent
    $.fn.fileInfo = (createOptionsOrAction, noneOrActionParams) ->
        $this = this

        componentOptions = {}
        actionParams = {}
        if typeof createOptionsOrAction is 'string'
            action = createOptionsOrAction
            actionParams = noneOrActionParams || {}
        else
            action = 'create'
            componentOptions = createOptionsOrAction || {}

        state = {
            file: {
                path: undefined
                sizeInBytes: undefined
                previewHtml: undefined
                accessRights: undefined #TODO
            }
        }

        defaultComponentOptions = {
            urlInfo: '/uploads/info'
            urlOperations: '/uploads/manage'
            callbackRenamed: () -> return
            callbackDeleted: () -> return
#            callbackFile: () -> return
            callbackAjaxError: () -> return #TODO method signature?
        }

        componentOptions = $.extend(true, defaultComponentOptions, componentOptions)

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

        render = () ->
            $this.html('')
            if ! state.file? || ! state.file.path?
                return

            file = state.file
            $this.append('<p><b>file path:</b> ' + file.path + '</p>')
            #TODO http://www.appelsiini.net/projects/jeditable
            if file.sizeInBytes?
                $this.append('<p><b>size:</b> ' + formatFileSize(file.sizeInBytes) + '</p>')
            if file.previewHtml?
                $this.append('<p><b>preview:</b> <div class="fileInfoPreview">' + file.previewHtml +'</div></p>')

        createComponent = () ->
            render()
            $this.data('options', componentOptions)

        selectFile = () ->
            filePath = undefined
            if typeof actionParams is 'string'
                filePath = actionParams
            else
                filePath = actionParams.filePath

            if ! filePath?
                throw new Error('filePath in action params must be defined')

            state.file = {path: filePath}
            render()

            $.ajax({
                type: "POST"
                url: componentOptions.urlInfo
                data: state.file
                success: (data) ->
                    state.file = data
                    render()
                dataType: 'json'
            });

        if action != 'create'
            componentOptions = $this.data('options')
            state = $this.data('state')

        switch action
            when 'selectFile' then selectFile()
            else
                createComponent()

        $this.data('state', state)
        return $this

    # главный компонент
    $.fn.fileDialog = (options) ->
        options = options || {}
        defaultOptions = {
            dialogTitle: 'File select',
            manualInput: false
            urlList: '/uploads/list'
            urlInfo: '/uploads/info'
            urlOperations: '/uploads/manage' # move, rename, delete
            urlJQueryFileUpload: '/uploads/handleJqueryFileUpload'
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
            },
            fileUploadSuccess: () ->
                return
            fileUploadError: () ->
                return
            # TODO translation
        }
        #TODO make from widget's `data-` attributes; class="jQueryFileDialog" runs functions automatically
        #TODO actions: openFileDialog, restoreOriginalHtml, getData - https://learn.jquery.com/plugins/basic-plugin-creation/
        #TODO configurable defaultOptions (dataTable ?)
        #TODO each!
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
        filesDropZoneId = fileInputId+'_fileDropZone'

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

        data.inputHtml = fileInput.html();
        $('#'+fileInputId).replaceAll($('#'+replaceMeId))
        $fileInput = $('#'+fileInputId)
        $fileInput.addClass('form-control')
        $fileInput.attr('type', 'text')

        # <input id="'+id+'" class="form-control" type="text">

        renderDropZoneLabel = (uploadFolder) ->
            return 'Click here or drag files to upload' + (if uploadFolder then ' to "'+uploadFolder+'"' else '...')

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
                                <span id="'+filesDropZoneId+'" class="fileinput-button dropzone">
                                    <i class="glyphicon glyphicon-plus"></i>
                                    <span class="dropZoneLabel"></span>
                                    <p><span class="releaseHereNote">(release files here to upload)</span></p>
                                    <!-- The file input field used as target for the file upload widget -->
                                    <input id="fileupload" type="file" name="files[]" multiple>
                                </span>
                                <!-- The global progress bar -->
                                <div id="progress" class="progress">
                                    <div class="progress-bar progress-bar-success"></div>
                                </div>
                                <!-- The container for the uploaded files -->
                                <!-- <div id="files" class="files"></div>-->
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
        $fileInfo = $('.fileInfo', $fileDialog)
        $fileTree = $('#'+fileTreeId, $fileDialog)
        $filesDropZone = $('#'+filesDropZoneId, $fileDialog)
        $filesDropZoneLabel = $('.dropZoneLabel', $filesDropZone)
        $filesDropZoneLabel.text(renderDropZoneLabel(options.selectedFolder))
        $selectedFolder = null

        fileTreeOptions = $.extend(true, options.fileTreeOptions, {
            root: '/'
            script: options.urlList
        })

        updateSelectedFolder = () ->
            $('.directory', $fileTree).removeClass('selectedFolder')
            $selectedFolder = $('.directory.expanded', $fileTree).last()
            if $selectedFolder? and $selectedFolder.length > 0
                $anchor = $selectedFolder.children('a').first()
                $selectedFolder.addClass('selectedFolder')
                data.selectedFolder = $anchor.attr('rel')
            else
                data.selectedFolder = ''
#            console.log data.selectedFolder
            $filesDropZoneLabel.text(renderDropZoneLabel(data.selectedFolder))
            uploadUrl = options.urlJQueryFileUpload
            if data.selectedFolder
                uploadUrl += '?folder=' + encodeURIComponent(data.selectedFolder)
            $filesDropZone.fileupload({
                url: uploadUrl
            })

        $fileInfo.fileInfo({
            urlInfo: options.urlInfo,
            urlOperations: options.urlOperations
        })

        reloadFileTree = () ->
            $fileTree.empty()
            $fileTree.data('fileTree', null)
            $fileTree.fileTree(fileTreeOptions, (file) ->
                $selectFileButton.show()
                data.selectedFile = file
                $fileInfo.fileInfo('selectFile', data.selectedFile)
                return
            ).on('filetreeexpanded', (e, data) -> updateSelectedFolder()
            ).on('filetreecollapsed', (e, data) -> updateSelectedFolder()
            );

        reloadFileTree()

        $selectFileButton.hide();
        $selectFileButton.on 'click', () ->
            $fileInput.val(data.selectedFile);
            $fileDialog.modal('hide')

        $filesDropZone.fileupload(
            url: options.urlJQueryFileUpload
            dataType: 'json'
            done: (e, data) ->
                $.each data.result.files, (index, file) ->
                    text = ''
                    if file.error
                        options.fileUploadError(file)
#                        text = '/!\\ ' + file.name + ': ' + file.error
                    else
                        options.fileUploadSuccess(file)
#                        text = file.name
                    $('<p/>').text(text).appendTo '#files'
                    return
                $('#progress .progress-bar').css 'visibility', 'hidden'
                if $selectedFolder? and $selectedFolder.length > 0
                    $_selectedFolder = $selectedFolder
                    # refresh node = collapse + expand = click + click
                    $_selectedFolder.children('a').click()
                    $_selectedFolder.children('a').click()
                else
                    reloadFileTree()
                return
            progressall: (e, data) ->
                progress = parseInt(data.loaded / data.total * 100, 10)
                $('#progress .progress-bar').css 'visibility', 'visible'
                $('#progress .progress-bar').css 'width', progress + '%'
                return
#            process: (e, data) ->
#                console.log('Processing ' + data.files[data.index].name + '...');
#                return

#            add: (e, data) ->
#                if e.isDefaultPrevented()
#                    return false
#                if data.autoUpload or data.autoUpload != false and $(this).fileupload('option', 'autoUpload')
#                    data.process().done ->
#                        data.submit()
#                        return
#                return

        ).error((jqXHR, textStatus, errorThrown) ->
            console.log 'Error: ' + textStatus
            console.log errorThrown
            return
        ).prop('disabled', !$.support.fileInput).parent().addClass if $.support.fileInput then undefined else 'disabled'
        $(document).bind 'dragover', (e) ->
            timeout = window.dropZoneTimeout

            if !timeout
                $filesDropZone.addClass 'in'
            else
                clearTimeout timeout

            found = false
            node = e.target
            loop
                if node == $filesDropZone[0]
                    found = true
                    break
                node = node.parentNode
                unless node != null
                    break

            window.dropZoneTimeout = setTimeout((->
                window.dropZoneTimeout = null
                $filesDropZone.removeClass 'in hover'
                return
            ), 200)
            return

        # TODO edit-in-place file info (access rights, path)
        # TODO so server passes json file info array to client, not rendered html

        # TODO reload jQueryFileTree every dialog open and after file move
        # TODO "upload file here" button
        # TODO highlight selected folder in file tree
        # TODO how to reload tree
    ) jQuery
# make file visible on source tree when dynamically loaded
`
//# sourceURL=jQueryFileDialog.js
//`
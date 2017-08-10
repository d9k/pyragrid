/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * DS207: Consider shorter variations of null checks
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
(function($) {

    // file info subcomponent
    $.fn.fileInfo = function(createOptionsOrAction, noneOrActionParams) {
        let action;
        const $this = this;

        let componentOptions = {};
        let actionParams = {};
        if (typeof createOptionsOrAction === 'string') {
            action = createOptionsOrAction;
            actionParams = noneOrActionParams || {};
        } else {
            action = 'create';
            componentOptions = createOptionsOrAction || {};
        }

        let state = {
            file: {
                path: undefined,
                sizeInBytes: undefined,
                previewHtml: undefined,
                accessRights: undefined //TODO
            }
        };

        const defaultComponentOptions = {
            urlInfo: '/uploads/info',
            urlOperations: '/uploads/manage',
            callbackRenamed(from, to) {  },
            callbackDeleted(path) {  },
//            callbackFile: () -> return
            callbackRenameError(from, to, e) {  },
            callbackDeleteError(path, e) {  }
        };

        componentOptions = $.extend(true, defaultComponentOptions, componentOptions);

        const formatFileSize = function(bytes, _1000) {
            let size = bytes;
            const divisor = _1000 ? 1000 : 1024;
            if (Math.abs(size) < divisor) {
                return size + ' B';
            }
            const units = _1000 ?
                ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
            :
                ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

            let unitIndex = -1;
            while (true) {
                size /= divisor;
                ++unitIndex;
                if ((Math.abs(size) <= divisor) || (unitIndex > (units.length - 1))) {
                    break;
                }
            }

            return size.toFixed(1) + ' ' + units[unitIndex];
        };

        var render = function() {
            $this.html('');
            if ((state.file == null) || (state.file.path == null)) {
                return;
            }

            const { file } = state;
            $this.append(
                `<p><b>file path:</b><br/> \
<span class="filePath edit-in-place" title="Click to move/rename" data-type="textarea"  data-ok-button="Move/Rename" data-cancel-button="Cancel">` +
                        file.path +
                   '</span>' +
                '</p>'
            );
            //TODO https://github.com/itinken/jinplace
            if (file.sizeInBytes != null) {
                $this.append(`<p><b>size:</b>${formatFileSize(file.sizeInBytes)}</p>`);
            }
            if (file.previewHtml != null) {
                $this.append(`<p><b>preview:</b> <div class="fileInfoPreview">${file.previewHtml(+'</div></p>')}`);
            }
            $this.append(`\
<button \
class="deleteFile btn btn-sm btn-danger" \
title="Delete file &quot;` + file.path + `&quot;?" \
data-toggle="confirmation" \
data-btn-ok-label="Delete!" \
data-btn-ok-icon="glyphicon glyphicon-remove" \
data-btn-ok-class="btn-danger" \
data-btn-cancel-label="Do nothing" \
data-btn-cancel-icon="glyphicon glyphicon-time" \
data-btn-cancel-class="btn-default" \
data-popout="true" \
data-placement="bottom" \
> \
<span class="glyphicon glyphicon-trash"></span> \
</button>`);

            $('.filePath.edit-in-place', $this).jinplace({
                submitFunction(opts, valueToPath) {
                    return $.ajax(componentOptions.urlOperations, {
                        type: "post",
                        data: {
                            action: 'move',
                            from: file.path,
                            to: valueToPath
                        },
                        dataType: 'text',
                        success(resultValue) {
                            const fromPath = file.path;
                            state.file = undefined;
                            render();
                            componentOptions.callbackRenamed(fromPath, resultValue);
                        },
                        error(e) {
                            // TODO check for errors handling
                            const fromPath = file.path;
                            componentOptions.callbackRenameError(fromPath, valueToPath, e);
                        }
                    });
                }

            });

            return $('button.deleteFile', $this).confirmation({
                onConfirm() {
                    return $.ajax(componentOptions.urlOperations, {
                        type: "post",
                        data: {
                            action: 'delete',
                            path: file.path
                        },
                        dataType: 'text',
                        success(resultValue) {
                            const deletedPath = file.path;
                            if (resultValue !== deletedPath) {
                                componentOptions.callbackDeleteError(deletedPath, e);
                                return;
                            }
                            state.file = undefined;
                            render();
                            componentOptions.callbackDeleted(deletedPath);
                        },
                        error(e) {
                            const deletedPath = file.path;
                            componentOptions.callbackDeleteError(deletedPath, e);
                        }
                    });
                }
            });
        };


        const createComponent = function() {
            render();
            return $this.data('options', componentOptions);
        };

        const selectFile = function() {
            let filePath = undefined;
            if (typeof actionParams === 'string') {
                filePath = actionParams;
            } else {
                ({ filePath } = actionParams);
            }

            if ((filePath == null)) {
                throw new Error('filePath in action params must be defined');
            }

            state.file = {path: filePath};
            render();

            return $.ajax({
                type: "POST",
                url: componentOptions.urlInfo,
                data: state.file,
                success(data) {
                    state.file = data;
                    return render();
                },
                dataType: 'json'
            });
        };

        if (action !== 'create') {
            componentOptions = $this.data('options');
            state = $this.data('state');
        }

        switch (action) {
            case 'selectFile': selectFile(); break;
            default:
                createComponent();
        }

        $this.data('state', state);
        return $this;
    };

    //#######################
    // Main Component
    //########################
    return $.fn.fileDialog = function(options) {
        options = options || {};
        const defaultOptions = {
            dialogTitle: 'File select',
            manualInput: false,
            urlList: '/uploads/list',
            urlInfo: '/uploads/info',
            urlOperations: '/uploads/manage', // move, rename, delete
            urlJQueryFileUpload: '/uploads/handleJqueryFileUpload',
// TODO           showFilesOrFolders: 'any' # 'any'|'files'|'folders'
// TODO           selectFilesOrFolders: 'file' # 'file'|'folder'|'none'
            // TODO 'file'|'files'|'folder'|'folders'|'none'
// TODO            showInfo: true
// TODO           showOperations: true
// TODO           showClear: true
// TODO           showDelete: true
// TODO           showUpload: true
            fileTreeOptions: {
                expandSpeed: 120,
                collapseSpeed: 120,
                multiFolder: false
            },
            fileUploadSuccess() {
            },
            fileUploadError() {
            }
            // TODO translation
        };
        //TODO check dependencies!!
        //TODO make from widget's `data-` attributes; class="jQueryFileDialog" runs functions automatically
        //TODO actions: openFileDialog, restoreOriginalHtml, getData - https://learn.jquery.com/plugins/basic-plugin-creation/
        //TODO configurable defaultOptions (dataTable ?)
        //TODO each!
        options = $.extend(true, defaultOptions, options);
        const data = {
            selectedFile: '',
            selectedFolder: '',
            inputHtml: '',
            fileInfo: {
                path: '',
                size: '',
                additionalHtml: ''
            }
        };

        const fileInput = this;
        const fileInputId = fileInput.attr('id');
        if (!fileInputId) {
            error('id of field is required');
            return;
        }
        const buttonClearId = fileInputId+'_clear';
        const replaceMeId = `replaceMeWith_${fileInputId}`;
        const buttonBrowseId = fileInputId+'_browse';
        const inputGroupId = fileInputId+'_group';
        const modalId = fileInputId+'_modal';
        const fileTreeId = fileInputId+'_fileTree';
        const filesDropZoneId = fileInputId+'_fileDropZone';

        const buttonClear = fileInput.next(`button#${buttonClearId}`);
        if (buttonClear.length) {
            error('file dialog already applied to field');
            return;
        }

        // TODO http://api.jquery.com/after/ - append buttons (clear/open dialog) next to element
        // TODO input groups http://getbootstrap.com/css/#forms-control-validation
        // TODO button groups http://getbootstrap.com/components/
        fileInput.after(`\
<div id="`+inputGroupId+`" class="input-group"> \
<div id="`+replaceMeId+`" /> \
<span class="input-group-btn"> \
<button id="`+buttonClearId+`" class="btn btn-default" type="button" title="Clear value"><span class="glyphicon glyphicon-remove"></span></button> \
<button id="`+buttonBrowseId+'" class="btn btn-default" type="button" title="Browse..." data-toggle="modal" data-target="#'+modalId+`"><span class="glyphicon glyphicon-folder-open"></span></button> \
</span> \
</div>\
`);

        data.inputHtml = fileInput.html();
        $(`#${fileInputId}`).replaceAll($(`#${replaceMeId}`));
        const $fileInput = $(`#${fileInputId}`);
        $fileInput.addClass('form-control');
        $fileInput.attr('type', 'text');

        $(`#${buttonClearId}`).click(function(e) {
            $fileInput.val('');
            return $fileInput.focus();
        });

        // <input id="'+id+'" class="form-control" type="text">

        const renderDropZoneLabel = uploadFolder => `Click here or drag files to upload${uploadFolder ? ` to "${uploadFolder}"` : '...'}`;

        $('body').prepend(`\
<div class="fileDialogModal modal fade" id="`+modalId+`" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"> \
<div class="modal-dialog" role="document"> \
<div class="modal-content"> \
<div class="modal-header"> \
<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
<h4 class="modal-title" id="myModalLabel">`+options.dialogTitle+`</h4> \
</div> \
<div class="modal-body"> \
<div class="row"> \
<div class="col-md-7"> \
<div class="column"> \
<span id="`+filesDropZoneId+`" class="fileinput-button dropzone"> \
<i class="glyphicon glyphicon-plus"></i> \
<span class="dropZoneLabel"></span> \
<p><span class="releaseHereNote">(release files here to upload)</span></p> \
<!-- The file input field used as target for the file upload widget --> \
<input id="fileupload" type="file" name="files[]" multiple> \
</span> \
<!-- The global progress bar --> \
<div id="progress" class="progress"> \
<div class="progress-bar progress-bar-success"></div> \
</div> \
<!-- The container for the uploaded files --> \
<!-- <div id="files" class="files"></div>--> \
<div class="fileTreeRoot" id="`+fileTreeId+`" ></div> \
</div> \
</div> \
<div class="col-md-5"> \
<div class="column"> \
<h3>File info</h3> \
<div class="fileInfo"> \
</div> \
</div> \
<div class="buttons"> \
<button type="button" class="btn btn-default" data-dismiss="modal">Close</button> \
<button type="button" class="btn btn-primary selectFileButton">Select file</button> \
</div> \
</div> \
</div> \
</div> \
</div> \
</div> \
</div>\
`);

        const $fileDialog = $(`#${modalId}`);
        const $selectFileButton = $('.selectFileButton', $fileDialog);
        const $fileInfo = $('.fileInfo', $fileDialog);
        const $fileTree = $(`#${fileTreeId}`, $fileDialog);
        const $filesDropZone = $(`#${filesDropZoneId}`, $fileDialog);
        const $filesDropZoneLabel = $('.dropZoneLabel', $filesDropZone);
        $filesDropZoneLabel.text(renderDropZoneLabel(options.selectedFolder));
        let $selectedFolder = null;

        const fileTreeOptions = $.extend(true, options.fileTreeOptions, {
            root: '/',
            script: options.urlList
        });

        const updateSelectedFolder = function() {
            $('.directory', $fileTree).removeClass('selectedFolder');
            $selectedFolder = $('.directory.expanded', $fileTree).last();
            if (($selectedFolder != null) && ($selectedFolder.length > 0)) {
                const $anchor = $selectedFolder.children('a').first();
                $selectedFolder.addClass('selectedFolder');
                data.selectedFolder = $anchor.attr('rel');
            } else {
                data.selectedFolder = '';
            }
//            console.log data.selectedFolder
            $filesDropZoneLabel.text(renderDropZoneLabel(data.selectedFolder));
            let uploadUrl = options.urlJQueryFileUpload;
            if (data.selectedFolder) {
                uploadUrl += `?folder=${encodeURIComponent(data.selectedFolder)}`;
            }
            return $filesDropZone.fileupload({
                url: uploadUrl
            });
        };

        const reloadFileTree = function() {
            $fileTree.empty();
            $fileTree.data('fileTree', null);
            return $fileTree.fileTree(fileTreeOptions, function(file) {
                $selectFileButton.show();
                data.selectedFile = file;
                $fileInfo.fileInfo('selectFile', data.selectedFile);
            }).on('filetreeexpanded', (e, data) => updateSelectedFolder()).on('filetreecollapsed', (e, data) => updateSelectedFolder());
        };

        $fileInfo.fileInfo({
            urlInfo: options.urlInfo,
            urlOperations: options.urlOperations,
            callbackRenamed(from, to) {
                // TODO make arg selectedNode
                return reloadFileTree();
            },
            callbackDeleted(path) {
                return reloadFileTree();
            }
        });

        reloadFileTree();

        $selectFileButton.hide();
        $selectFileButton.on('click', function() {
            $fileInput.val(data.selectedFile);
            return $fileDialog.modal('hide');
        });

        $filesDropZone.fileupload({
            url: options.urlJQueryFileUpload,
            dataType: 'json',
            done(e, data) {
                $.each(data.result.files, function(index, file) {
                    const text = '';
                    if (file.error) {
                        options.fileUploadError(file);
//                        text = '/!\\ ' + file.name + ': ' + file.error
                    } else {
                        options.fileUploadSuccess(file);
                    }
//                        text = file.name
                    $('<p/>').text(text).appendTo('#files');
                });
                $('#progress .progress-bar').css('visibility', 'hidden');
                if (($selectedFolder != null) && ($selectedFolder.length > 0)) {
                    const $_selectedFolder = $selectedFolder;
                    // refresh node = collapse + expand = click + click
                    $_selectedFolder.children('a').click();
                    $_selectedFolder.children('a').click();
                } else {
                    reloadFileTree();
                }
            },
            progressall(e, data) {
                const progress = parseInt((data.loaded / data.total) * 100, 10);
                $('#progress .progress-bar').css('visibility', 'visible');
                $('#progress .progress-bar').css('width', progress + '%');
            }
//            process: (e, data) ->
//                console.log('Processing ' + data.files[data.index].name + '...');
//                return

//            add: (e, data) ->
//                if e.isDefaultPrevented()
//                    return false
//                if data.autoUpload or data.autoUpload != false and $(this).fileupload('option', 'autoUpload')
//                    data.process().done ->
//                        data.submit()
//                        return
//                return

        }).error(function(jqXHR, textStatus, errorThrown) {
            console.log(`Error: ${textStatus}`);
            console.log(errorThrown);
        }).prop('disabled', !$.support.fileInput).parent().addClass($.support.fileInput ? undefined : 'disabled');
        return $(document).bind('dragover', function(e) {
            const timeout = window.dropZoneTimeout;

            if (!timeout) {
                $filesDropZone.addClass('in');
            } else {
                clearTimeout(timeout);
            }

            let found = false;
            let node = e.target;
            while (true) {
                if (node === $filesDropZone[0]) {
                    found = true;
                    break;
                }
                node = node.parentNode;
                if (node === null) {
                    break;
                }
            }

            window.dropZoneTimeout = setTimeout((function() {
                window.dropZoneTimeout = null;
                $filesDropZone.removeClass('in hover');
            }), 200);
        });
    };

        // TODO edit-in-place file info (access rights, path)
        // TODO so server passes json file info array to client, not rendered html

        // TODO reload jQueryFileTree every dialog open and after file move
        // TODO "upload file here" button
        // TODO highlight selected folder in file tree
        // TODO how to reload tree
    })(jQuery);
// make file visible on source tree when dynamically loaded

//# sourceURL=jQueryFileDialog.js
//;
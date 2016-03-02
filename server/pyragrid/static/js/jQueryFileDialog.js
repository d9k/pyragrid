(function() {
  (function($) {
    return $.fn.fileDialog = function(options) {
      var $fileDialog, $fileInfo, $fileInput, $fileTree, $filesDropZone, $filesDropZoneLabel, $selectFileButton, $selectedFolder, buttonBrowseId, buttonClear, buttonClearId, data, defaultOptions, fileInput, fileInputId, fileTreeId, fileTreeOptions, filesDropZoneId, formatFileSize, inputGroupId, modalId, reloadFileTree, renderDropZoneLabel, renderFileInfo, replaceMeId, updateSelectedFolder;
      options = options || {};
      defaultOptions = {
        dialogTitle: 'File select',
        manualInput: false,
        urlList: '/uploads/list',
        urlInfo: '/uploads/info',
        urlOperations: '/uploads/manage',
        urlJQueryFileUpload: '/uploads/handleJqueryFileUpload',
        fileTreeOptions: {
          expandSpeed: 120,
          collapseSpeed: 120,
          multiFolder: false
        },
        fileUploadSuccess: function() {},
        fileUploadError: function() {}
      };
      options = $.extend(true, defaultOptions, options);
      data = {
        selectedFile: '',
        selectedFolder: '',
        inputHtml: '',
        fileInfo: {
          path: '',
          size: '',
          additionalHtml: ''
        }
      };
      fileInput = this;
      fileInputId = fileInput.attr('id');
      if (!fileInputId) {
        error('id of field is required');
        return;
      }
      buttonClearId = fileInputId + '_clear';
      replaceMeId = 'replaceMeWith_' + fileInputId;
      buttonBrowseId = fileInputId + '_browse';
      inputGroupId = fileInputId + '_group';
      modalId = fileInputId + '_modal';
      fileTreeId = fileInputId + '_fileTree';
      filesDropZoneId = fileInputId + '_fileDropZone';
      buttonClear = fileInput.next('button#' + buttonClearId);
      if (buttonClear.length) {
        error('file dialog already applied to field');
        return;
      }
      fileInput.after('<div id="' + inputGroupId + '" class="input-group"> <div id="' + replaceMeId + '" /> <span class="input-group-btn"> <button id="' + buttonClearId + '" class="btn btn-default" type="button" title="Clear value"><span class="glyphicon glyphicon-remove"></span></button> <button id="' + buttonBrowseId + '" class="btn btn-default" type="button" title="Browse..." data-toggle="modal" data-target="#' + modalId + '"><span class="glyphicon glyphicon-folder-open"></span></button> </span> </div>');
      formatFileSize = function(bytes, _1000) {
        var divisor, size, unitIndex, units;
        size = bytes;
        divisor = _1000 ? 1000 : 1024;
        if (Math.abs(size) < divisor) {
          return size + ' B';
        }
        units = _1000 ? ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'] : ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        unitIndex = -1;
        while (true) {
          size /= divisor;
          ++unitIndex;
          if (Math.abs(size) <= divisor || unitIndex > units.length - 1) {
            break;
          }
        }
        return size.toFixed(1) + ' ' + units[unitIndex];
      };
      data.inputHtml = fileInput.html();
      $('#' + fileInputId).replaceAll($('#' + replaceMeId));
      $fileInput = $('#' + fileInputId);
      $fileInput.addClass('form-control');
      $fileInput.attr('type', 'text');
      renderDropZoneLabel = function(uploadFolder) {
        return 'Click here or drag files to upload' + (uploadFolder ? ' to "' + uploadFolder + '"' : '...');
      };
      $('body').prepend('<div class="fileDialogModal modal fade" id="' + modalId + '" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"> <div class="modal-dialog" role="document"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button> <h4 class="modal-title" id="myModalLabel">' + options.dialogTitle + '</h4> </div> <div class="modal-body"> <div class="row"> <div class="col-md-7"> <div class="column"> <span id="' + filesDropZoneId + '" class="fileinput-button dropzone"> <i class="glyphicon glyphicon-plus"></i> <span class="dropZoneLabel"></span> <p><span class="releaseHereNote">(release files here to upload)</span></p> <!-- The file input field used as target for the file upload widget --> <input id="fileupload" type="file" name="files[]" multiple> </span> <!-- The global progress bar --> <div id="progress" class="progress"> <div class="progress-bar progress-bar-success"></div> </div> <!-- The container for the uploaded files --> <!-- <div id="files" class="files"></div>--> <div class="fileTreeRoot" id="' + fileTreeId + '" ></div> </div> </div> <div class="col-md-5"> <div class="column"> <h3>File info</h3> <div class="fileInfo"> </div> </div> <div class="buttons"> <button type="button" class="btn btn-default" data-dismiss="modal">Close</button> <button type="button" class="btn btn-primary selectFileButton">Select file</button> </div> </div> </div> </div> </div> </div> </div>');
      $fileDialog = $('#' + modalId);
      $selectFileButton = $('.selectFileButton', $fileDialog);
      $fileInfo = $('.fileInfo', $fileDialog);
      $fileTree = $('#' + fileTreeId, $fileDialog);
      $filesDropZone = $('#' + filesDropZoneId, $fileDialog);
      $filesDropZoneLabel = $('.dropZoneLabel', $filesDropZone);
      $filesDropZoneLabel.text(renderDropZoneLabel(options.selectedFolder));
      $selectedFolder = null;
      fileTreeOptions = $.extend(true, options.fileTreeOptions, {
        root: '/',
        script: options.urlList
      });
      renderFileInfo = function(data) {
        var html;
        if (!data.path) {
          return 'Error: no data.path set';
        }
        html = '<p><b>file path:</b> ' + data.path + '</p>';
        if (data.size) {
          html += '<p><b>size:</b> ' + formatFileSize(data.size) + '</p>';
        }
        return html;
      };
      updateSelectedFolder = function() {
        var $anchor, uploadUrl;
        $('.directory', $fileTree).removeClass('selectedFolder');
        $selectedFolder = $('.directory.expanded', $fileTree).last();
        if (($selectedFolder != null) && $selectedFolder.length > 0) {
          $anchor = $selectedFolder.children('a').first();
          $selectedFolder.addClass('selectedFolder');
          data.selectedFolder = $anchor.attr('rel');
        } else {
          data.selectedFolder = '';
        }
        $filesDropZoneLabel.text(renderDropZoneLabel(data.selectedFolder));
        uploadUrl = options.urlJQueryFileUpload;
        if (data.selectedFolder) {
          uploadUrl += '?folder=' + encodeURIComponent(data.selectedFolder);
        }
        return $filesDropZone.fileupload({
          url: uploadUrl
        });
      };
      reloadFileTree = function() {
        $fileTree.empty();
        $fileTree.data('fileTree', null);
        return $fileTree.fileTree(fileTreeOptions, function(file) {
          $selectFileButton.show();
          data.selectedFile = file;
          $fileInfo.html(renderFileInfo({
            path: file
          }));
          $.ajax({
            type: "POST",
            url: options.urlInfo,
            data: {
              path: file
            },
            success: function(data) {
              return $fileInfo.html(renderFileInfo(data));
            },
            dataType: 'json'
          });
        }).on('filetreeexpanded', function(e, data) {
          return updateSelectedFolder();
        }).on('filetreecollapsed', function(e, data) {
          return updateSelectedFolder();
        });
      };
      reloadFileTree();
      $selectFileButton.hide();
      $selectFileButton.on('click', function() {
        $fileInput.val(data.selectedFile);
        return $fileDialog.modal('hide');
      });
      $filesDropZone.fileupload({
        url: options.urlJQueryFileUpload,
        dataType: 'json',
        done: function(e, data) {
          var $_selectedFolder;
          $.each(data.result.files, function(index, file) {
            var text;
            text = '';
            if (file.error) {
              options.fileUploadError(file);
            } else {
              options.fileUploadSuccess(file);
            }
            $('<p/>').text(text).appendTo('#files');
          });
          $('#progress .progress-bar').css('visibility', 'hidden');
          if (($selectedFolder != null) && $selectedFolder.length > 0) {
            $_selectedFolder = $selectedFolder;
            $_selectedFolder.children('a').click();
            $_selectedFolder.children('a').click();
          } else {
            reloadFileTree();
          }
        },
        progressall: function(e, data) {
          var progress;
          progress = parseInt(data.loaded / data.total * 100, 10);
          $('#progress .progress-bar').css('visibility', 'visible');
          $('#progress .progress-bar').css('width', progress + '%');
        }
      }).error(function(jqXHR, textStatus, errorThrown) {
        console.log('Error: ' + textStatus);
        console.log(errorThrown);
      }).prop('disabled', !$.support.fileInput).parent().addClass($.support.fileInput ? void 0 : 'disabled');
      return $(document).bind('dragover', function(e) {
        var found, node, timeout;
        timeout = window.dropZoneTimeout;
        if (!timeout) {
          $filesDropZone.addClass('in');
        } else {
          clearTimeout(timeout);
        }
        found = false;
        node = e.target;
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
  })(jQuery);

  
//# sourceURL=jQueryFileDialog.js
//;

}).call(this);

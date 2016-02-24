(function() {
  (function($) {
    return $.fn.fileDialog = function(options) {
      var $fileDialog, $fileInfo, $fileInput, $selectFileButton, buttonBrowseId, buttonClear, buttonClearId, data, defaultOptions, fileInput, fileTreeId, fileTreeOptions, id, inputGroupId, modalId, t;
      options = options | {};
      defaultOptions = {
        dialogTitle: 'File select',
        manualInput: false,
        urlList: '/uploads/list',
        urlInfo: '/uploads/info',
        urlOperations: '/uploads/manage',
        urlUpload: '/uploads/upload',
        fileTreeOptions: {
          expandSpeed: 120,
          collapseSpeed: 120,
          multiFolder: false
        }
      };
      options = $.extend(true, defaultOptions, options);
      data = {
        selectedFile: '',
        selectedFolder: ''
      };
      fileInput = this;
      id = fileInput.attr('id');
      if (!id) {
        error('id of field is required');
        return;
      }
      buttonClearId = id + '_clear';
      buttonBrowseId = id + '_browse';
      inputGroupId = id + '_group';
      modalId = id + '_modal';
      fileTreeId = id + '_fileTree';
      buttonClear = fileInput.next('button#' + buttonClearId);
      if (buttonClear.length) {
        error('file dialog already applied to field');
        return;
      }
      fileInput.replaceWith('<div id="' + inputGroupId + '" class="input-group"> <input id="' + id + '" class="form-control" type="text"> <span class="input-group-btn"> <button id="' + buttonClearId + '" class="btn btn-default" type="button" title="Clear value"><span class="glyphicon glyphicon-remove"></span></button> <button id="' + buttonBrowseId + '" class="btn btn-default" type="button" title="Browse..." data-toggle="modal" data-target="#' + modalId + '"><span class="glyphicon glyphicon-folder-open"></span></button> </span> </div>');
      fileInput.replaceWith('<div id="test_azaza">test</div>');
      t = 1;
      $('body').prepend('<div class="fileDialogModal modal fade" id="' + modalId + '" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"> <div class="modal-dialog" role="document"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button> <h4 class="modal-title" id="myModalLabel">' + options.dialogTitle + '</h4> </div> <div class="modal-body"> <div class="row"> <div class="col-md-7"> <div class="column"> <div class="fileTreeRoot" id="' + fileTreeId + '" ></div> </div> </div> <div class="col-md-5"> <div class="column"> <h3>File info</h3> <div class="fileInfo"> </div> </div> <div class="buttons"> <button type="button" class="btn btn-default" data-dismiss="modal">Close</button> <button type="button" class="btn btn-primary selectFileButton">Select file</button> </div> </div> </div> </div> </div> </div> </div>');
      $fileInput = $('#' + id);
      $fileDialog = $('#' + modalId);
      $selectFileButton = $('.selectFileButton', $fileDialog);
      $fileInfo = $('.fileInfo', $fileInfo);
      fileTreeOptions = $.extend(true, options.fileTreeOptions, {
        root: '/',
        script: options.urlList
      });
      $('#' + fileTreeId).fileTree(fileTreeOptions, function(file) {
        $selectFileButton.show();
        data.selectedFile = file;
        $fileInfo.html('');
        $.ajax({
          type: "POST",
          url: options.urlInfo,
          data: {
            filePath: file
          },
          success: function(data) {
            return $fileInfo.html(data);
          },
          dataType: 'html'
        });
      });
      $selectFileButton.hide();
      return $selectFileButton.on('click', function() {
        $fileInput.val(data.selectedFile);
        return $fileDialog.modal('hide');
      });
    };
  })(jQuery);

  
//# sourceURL=jQueryFileDialog.js
//;

}).call(this);

(function() {
  (function($) {
    return $.fn.fileDialog = function(options) {
      var buttonBrowseId, buttonClear, buttonClearId, defaultOptions, fileInput, id, inputGroupId, modalId, t;
      options = options | {};
      defaultOptions = {
        dialogTitle: 'File select',
        manualInput: false,
        urlList: '/uploads/list',
        urlInfo: '/uploads/info',
        urlOperations: '/uploads/manage',
        showFilesOrFolders: 'both',
        selectFilesOrFolders: 'files',
        showInfo: true,
        showOperations: true,
        showClear: true,
        showDelete: true
      };
      options = $.extend(true, defaultOptions, options);
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
      buttonClear = fileInput.next('button#' + buttonClearId);
      if (buttonClear.length) {
        error('file dialog already applied to field');
        return;
      }
      fileInput.replaceWith('<div id="' + inputGroupId + '" class="input-group"> <input id="' + id + '" class="form-control" type="text"> <span class="input-group-btn"> <button id="' + buttonClearId + '" class="btn btn-default" type="button" title="Clear value"><span class="glyphicon glyphicon-remove"></span></button> <button id="' + buttonBrowseId + '" class="btn btn-default" type="button" title="Browse..." data-toggle="modal" data-target="#' + modalId + '"><span class="glyphicon glyphicon-folder-open"></span></button> </span> </div>');
      fileInput.replaceWith('<div id="test_azaza">test</div>');
      t = 1;
      return $('body').prepend('<div class="modal fade" id="' + modalId + '" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"> <div class="modal-dialog" role="document"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button> <h4 class="modal-title" id="myModalLabel">' + options.dialogTitle + '</h4> </div> <div class="modal-body"> ... </div> <div class="modal-footer"> <button type="button" class="btn btn-default" data-dismiss="modal">Close</button> <button type="button" class="btn btn-primary">Save changes</button> </div> </div> </div> </div>');
    };
  })(jQuery);

  
//# sourceURL=jQueryFileDialog.js
//;

}).call(this);

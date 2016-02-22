(($) ->
    $.fn.fileDialog = (options) ->
        options = options | {}
        defaultOptions = {
            dialogTitle: 'File select',
            manualInput: false
            urlList: '/uploads/list'
            urlInfo: '/uploads/info'
            urlOperations: '/uploads/manage'
            showFilesOrFolders: 'both' # 'both'|'files'|'folders'
            selectFilesOrFolders: 'files'
            showInfo: true
            showOperations: true
            showClear: true
            showDelete: true
            # TODO translation
        }
        #TODO make from widget's `data-` attributes; class="jQueryFileDialog" runs functions automatically
        #TODO actions: openFileDialog, reset
        options = $.extend(true, defaultOptions, options)
#        this.html()

        fileInput = this
        id = fileInput.attr('id')
        if not id
            error 'id of field is required'
            return
        buttonClearId = id+'_clear'
        buttonBrowseId = id+'_browse'
        inputGroupId = id+'_group'
        modalId = id+'_modal'

        buttonClear = fileInput.next('button#' + buttonClearId)
        if buttonClear.length
            error 'file dialog already applied to field'
            return

        # TODO http://api.jquery.com/after/ - append buttons (clear/open dialog) next to element
        # TODO input groups http://getbootstrap.com/css/#forms-control-validation
        # TODO button groups http://getbootstrap.com/components/
        fileInput.replaceWith('
            <div id="'+inputGroupId+'" class="input-group">
              <input id="'+id+'" class="form-control" type="text">
              <span class="input-group-btn">
                <button id="'+buttonClearId+'" class="btn btn-default" type="button" title="Clear value"><span class="glyphicon glyphicon-remove"></span></button>
                <button id="'+buttonBrowseId+'" class="btn btn-default" type="button" title="Browse..." data-toggle="modal" data-target="#'+modalId+'"><span class="glyphicon glyphicon-folder-open"></span></button>
              </span>
            </div>
        ')

        fileInput.replaceWith('<div id="test_azaza">test</div>');

        # TODO http://api.jquery.com/prepend/ - append bootstrap overlay dialog
        # TODO
        t = 1
        #this.changer = $( "<button>", {
        #  text: "change",
        #  "class": "custom-colorize-changer"
        #})
        #.appendTo( this.element )
        #$('#fileTreeFileSelect').fileTree({
        #    root: '/',
        #    script: '{{ request.route_url('test_ajax_filetree') }}',
        #    expandSpeed: 120,
        #    collapseSpeed: 120,
        #    multiFolder: false
        #}, function(file) {
        #    alert(file);
        #});

        $('body').prepend('
            <div class="modal fade" id="'+modalId+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
              <div class="modal-dialog" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h4 class="modal-title" id="myModalLabel">'+options.dialogTitle+'</h4>
                  </div>
                  <div class="modal-body">
                    ...
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary">Save changes</button>
                  </div>
                </div>
              </div>
            </div>
        ')

    ) jQuery
# make file visible on source tree when dynamically loaded
`
//# sourceURL=jQueryFileDialog.js
//`
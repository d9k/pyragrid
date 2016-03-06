from deform.widget import Widget
from colander import null
from pyramid.threadlocal import get_current_request
import json


# TODO code just copied from TextInputWidget, transform to FileTree
class FileDialog(Widget):
    """
    Renders an ``<input type="text"/>`` widget.

    **Attributes/Arguments**

    template
       The template name used to render the widget.  Default:
        ``textinput``.

    readonly_template
        The template name used to render the widget in read-only mode.
        Default: ``readonly/textinput``.

    strip
        If true, during deserialization, strip the value of leading
        and trailing whitespace (default ``True``).

    mask
        A :term:`jquery.maskedinput` input mask, as a string.

        a - Represents an alpha character (A-Z,a-z)
        9 - Represents a numeric character (0-9)
        * - Represents an alphanumeric character (A-Z,a-z,0-9)

        All other characters in the mask will be considered mask
        literals.

        Example masks:

          Date: 99/99/9999

          US Phone: (999) 999-9999

          US SSN: 999-99-9999

        When this option is used, the :term:`jquery.maskedinput`
        library must be loaded into the page serving the form for the
        mask argument to have any effect.  See :ref:`masked_input`.

    mask_placeholder
        The placeholder for required nonliteral elements when a mask
        is used.  Default: ``_`` (underscore).

    """
    template = 'pyragrid:templates/deform_mod/file_dialog.pt'
    readonly_template = 'readonly/textinput'
    strip = True
    requirements = ( ('jquery.maskedinput', None), )

    def serialize(self, field, cstruct, **kw):
        if cstruct in (null, None):
            cstruct = ''
        readonly = kw.get('readonly', self.readonly)
        template = readonly and self.readonly_template or self.template
        values = self.get_template_values(field, cstruct, kw)
        request = get_current_request()
        # TODO restructure resources load. Must be ajax and non-dependant on pyragrid
        values['resourcesJson'] = json.dumps([
            # fileTree
            request.static_url('pyragrid:static/jqueryfiletree/jQueryFileTree.min.css'),
            request.static_url('pyragrid:static/jqueryfiletree/jQueryFileTree.min.js'),
            request.static_url('pyragrid:static/jqueryfiletree/jQueryFileTree.js'),
            # fileDialog
            request.static_url('pyragrid:static/jquery.ui.widget.js'),
            request.static_url('pyragrid:static/jquery.iframe-transport.js'),
            request.static_url('pyragrid:static/jquery.fileupload.js'),
            request.static_url('pyragrid:static/jquery.fileupload-mod.css'),
            request.static_url('pyragrid:static/js/jQueryFileDialog.js'),
            request.static_url('pyragrid:static/jinplace.js'),
            request.static_url('pyragrid:static/bootstrap-confirmation.js'),
            request.static_url('pyragrid:static/jQueryFileDialog.css')
        ])

        #TODO  '{{ request.static_url('pyragrid:static/jquery.fileupload.js') }}',
        return field.renderer(template, **values)

    def deserialize(self, field, pstruct):
        if pstruct is null:
            return null
        if self.strip:
            pstruct = pstruct.strip()
        if not pstruct:
            return null
        return pstruct
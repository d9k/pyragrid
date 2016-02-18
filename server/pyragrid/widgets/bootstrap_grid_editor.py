import deform.widget
from colander import null


class BootstrapGridEditor(deform.widget.TextAreaWidget):
    """https://github.com/Frontwise/grid-editor"""
    template = 'pyragrid:templates/deform_mod/grid_editor.pt'
    # readonly_template = 'readonly/textinput'

    def serialize(self, field, cstruct, **kw):
        if cstruct in (null, None):
            cstruct = ''
        readonly = kw.get('readonly', self.readonly)
        template = readonly and self.readonly_template or self.template
        values = self.get_template_values(field, cstruct, kw)
        try:
            values['oid'] = values['oid']
        except KeyError:
            values['oid'] = values['field'].oid

        values['gridId'] = values['oid']
        values['gridId'] += 'Grid'

        try:
            values['style'] = values['style']
        except KeyError:
            values['style'] = values['field'].widget.style

        # TODO to string or to list?
        if values['style'] is None:
            values['style'] = ''

        values['style'] += 'display:none'

        return field.renderer(template, **values)

import deform.widget
from colander import null


class TextInputPlaceholderWidget(deform.widget.TextInputWidget):
    placeholder = ''
    template = 'pyragrid:templates/deform_mod/textinputplaceholder.pt'

    def serialize(self, field, cstruct, **kw):
        if cstruct in (null, None):
            cstruct = ''
        readonly = kw.get('readonly', self.readonly)
        template = readonly and self.readonly_template or self.template
        values = self.get_template_values(field, cstruct, kw)
        # hack for placeholder working
        values['placeholder'] = self.placeholder
        return field.renderer(template, **values)


class PasswordPlaceholderWidget(TextInputPlaceholderWidget):
    placeholder = ''
    template = 'pyragrid:templates/deform_mod/passwordplaceholder.pt'
    # TODO fix readonly
    readonly_template = 'readonly/password'
    redisplay = False
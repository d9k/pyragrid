from . import TextInputPlaceholderWidget
from colander import null


class OrderEmailWidget(TextInputPlaceholderWidget):
    template = 'pyragrid:templates/deform_mod/order_email.pt'
    readonly_template = 'pyragrid:templates/deform_mod/readonly/order_email.pt'
    logout_url = None

    def serialize(self, field, cstruct, **kw):
        if cstruct in (null, None):
            cstruct = ''
        readonly = kw.get('readonly', self.readonly)
        template = readonly and self.readonly_template or self.template
        values = self.get_template_values(field, cstruct, kw)
        # hack for placeholder working
        values['placeholder'] = self.placeholder
        values['logout_url'] = self.logout_url
        return field.renderer(template, **values)


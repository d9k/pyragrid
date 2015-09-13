import deform
from colander import (
    Schema,
    SchemaNode,
    String,
    null
)
from deform import widget


class PlaceHolderTextInput(widget.TextInputWidget):
    placeholder = ''
    template = 'best_tests_server:templates/deform_mod/textinputplaceholder.pt'

    def serialize(self, field, cstruct, **kw):
        if cstruct in (null, None):
            cstruct = ''
        readonly = kw.get('readonly', self.readonly)
        template = readonly and self.readonly_template or self.template
        values = self.get_template_values(field, cstruct, kw)
        # hack for placeholder working
        values['placeholder'] = self.placeholder
        return field.renderer(template, **values)

    def deserialize(self, field, pstruct):
        return super(PlaceHolderTextInput, self).deserialize(field, pstruct)


class LoginSchema(Schema):

    login = SchemaNode(
        String(),
        title='Логин',
        # subject='Login'
        widget=PlaceHolderTextInput(
            placeholder='email, id вконтакте или ник',
        ),
    )

    password = SchemaNode(
        String(),
        title='Пароль',
        widget=deform.widget.PasswordWidget(size=20),
        description='Пароль к аккаунту',
    )

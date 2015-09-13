import deform
import colander
from colander import (
    Schema,
    SchemaNode,
    String,
    null
)
from deform import (
    widget,
    Button
)

class TextInputPlaceHolderWidget(widget.TextInputWidget):
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


class PasswordPlaceholderWidget(TextInputPlaceHolderWidget):
    placeholder = ''
    template = 'best_tests_server:templates/deform_mod/passwordplaceholder.pt'
    readonly_template = 'readonly/password'
    redisplay = False





class LoginSchema(Schema):
    # validator = self.validate_user_exists
    # def __init__(self):
    #     super(LoginSchema, self).__init__(validator=self.validate_auth)

    user = None

    # validator = validate_user_exists

    login = SchemaNode(
        String(),
        title='Логин',
        # subject='Login'
        widget=TextInputPlaceHolderWidget(
            placeholder='email, id вконтакте или ник'
        ),
    )



    password = SchemaNode(
        String(),
        title='Пароль',
        placeholder='*****',
        widget=PasswordPlaceholderWidget(placeholder='*****'),
    )

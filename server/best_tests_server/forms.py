import colander
from colanderalchemy import SQLAlchemySchemaNode

from colander import (
    Schema,
    SchemaNode,
    String,
    null
)
import best_tests_server.models as models
from .widgets import TextInputPlaceHolderWidget, PasswordPlaceholderWidget, RecaptchaWidget


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


def create_edit_user_schema():
    return SQLAlchemySchemaNode(models.User)


class RegisterSchema(SQLAlchemySchemaNode):

    def __init__(self, class_=models.User, includes=None,
                 excludes=None, overrides=None, unknown='ignore', **kw):
        if includes is None:
            includes = ['login', 'name', 'email', 'password_hash']
        super().__init__(models.User,
                         includes=includes,
                         **kw)
        self.add(colander.SchemaNode(
            colander.String(),
            title='Капча',
            # widget=RecaptchaWidget(lang='ru', theme='clean'),
            widget=RecaptchaWidget(lang='ru', theme='clean'),
            order=1000
        ))
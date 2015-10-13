import colander
from colanderalchemy import SQLAlchemySchemaNode

from colander import (
    Schema,
    SchemaNode,
    String,
    null
)
import deform.widget as widgets
import best_tests_server.models as models
from .widgets import TextInputPlaceHolderWidget, PasswordPlaceholderWidget, RecaptchaWidget
from .helpers import check_dev_mode

class LoginSchema(Schema):
    login = SchemaNode(
        String(),
        title='Логин',
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
                 excludes=None,
                 overrides=None,
                 unknown='ignore', **kw):
        if includes is None:
            includes = ['login', 'name', 'email']
        super().__init__(class_,
                         includes=includes,
                         overrides=overrides,
                         **kw)
        self.add(SchemaNode(
            String(),
            name='password',
            title='Пароль',
            widget=widgets.CheckedPasswordWidget(
                placeholder='email, id вконтакте или ник'
            ),
            missing=None
        ))
        if not check_dev_mode():
            self.add(SchemaNode(
                colander.String(),
                title='Капча',
                widget=RecaptchaWidget(lang='ru', theme='clean'),
                order=1000
            ))


class ProfileEditSchema(SQLAlchemySchemaNode):

    def __init__(self, class_=models.User, includes=None,
                 excludes=None,
                 overrides=None,
                 unknown='ignore', **kw):
        if includes is None:
            includes = ['name', ]
        super().__init__(class_,
                     includes=includes,
                     overrides=overrides,
                     **kw)

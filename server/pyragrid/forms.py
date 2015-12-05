import colander
from colanderalchemy import SQLAlchemySchemaNode

from colander import (
    Schema,
    SchemaNode,
    String,
    null
)
import deform.widget as widgets
from pyragrid import models, helpers
from .widgets import (
    TextInputPlaceHolderWidget,
    PasswordPlaceholderWidget,
    RecaptchaWidget,
    exception_for_schema_field
)
from .helpers import check_dev_mode
from .models import User

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


def user_login_unique_validator(node, value):
    found = User.by_login(value)
    if found is not None:
        raise colander.Invalid(node, 'Пользователь с таким логином уже существует')


def email_unique_validator(node, value):
    found = User.by_email(value)
    if found is not None:
        raise colander.Invalid(node, 'Пользователь с таким адресом уже существует')


# TODO @deferred
def validate_user_edit_form(schema, values):
    # found = User.by_login(value)
    linked_user = None
    not_id = None
    if hasattr(schema, 'linked_user'):
        linked_user = schema.linked_user
    if linked_user is not None:
        not_id = linked_user.id
    found_by_login = User.by_login(values.get('login'), not_id)
    if found_by_login is not None:
        raise exception_for_schema_field(schema, 'login', 'Пользователь с таким логином уже существует')
    found_by_email = User.by_email(values.get('email'), not_id)
    if found_by_email is not None:
        raise exception_for_schema_field(schema, 'email', 'Пользователь с таким адресом уже существует')


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
        self.validator = validate_user_edit_form


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
        self.linked_user = None
        self.validator = validate_user_edit_form


class UserEditSchema(SQLAlchemySchemaNode):
    def __init__(self, class_=models.User, includes=None,
                 excludes=None,
                 overrides=None,
                 unknown='ignore', **kw):
        if includes is None:
            includes = ['login', 'vk_id',  'name', 'email', 'active', 'email_checked']
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
        self.linked_user = None
        self.validator = validate_user_edit_form
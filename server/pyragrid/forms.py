import colander
from colanderalchemy import SQLAlchemySchemaNode

from colander import (
    Schema,
    SchemaNode,
    String,
    null
)
import deform.widget as widgets
from pyragrid import db, helpers
from .widgets import (
    TextInputPlaceholderWidget,
    PasswordPlaceholderWidget,
    RecaptchaWidget,
    BootstrapGridEditor,
    exception_for_schema_field,
    OrderEmailWidget
)
from .helpers import check_dev_mode
from .db import (
    User,
    Article,
    Good
)


class LoginSchema(Schema):
    login = SchemaNode(
        String(),
        title='Логин',
        widget=TextInputPlaceholderWidget(
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
    return SQLAlchemySchemaNode(db.User)


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


def validate_article_edit_form(schema, values):
    # found = User.by_login(value)
    linked_article = None
    not_id = None
    if hasattr(schema, 'linked_article'):
        linked_article = schema.linked_article
    if linked_article is not None:
        not_id = linked_article.id
    found_by_system_name = Article.by_system_name(values.get('system_name'), not_id)
    if found_by_system_name is not None:
        raise exception_for_schema_field(schema, 'system_name', 'Статья с таким системным именем уже существует')
    found_by_path = Article.by_path(values.get('path'), not_id)
    if found_by_path is not None:
        raise exception_for_schema_field(schema, 'path', 'Статья с таким путём уже существует')


class RegisterSchema(SQLAlchemySchemaNode):

    def __init__(self, class_=db.User, includes=None,
                 excludes=None,
                 overrides=None,
                 unknown='ignore', **kw):
        if includes is None:
            includes = ['login', 'name', 'email']
        super().__init__(class_, includes=includes, overrides=overrides, excludes=excludes, unknown=unknown, **kw)
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
    def __init__(self, class_=db.User, includes=None,
                 excludes=None,
                 overrides=None,
                 unknown='ignore', **kw):
        if includes is None:
            includes = ['name', ]
        super().__init__(class_, includes=includes, overrides=overrides, excludes=excludes, unknown=unknown, **kw)
        self.linked_user = None
        self.validator = validate_user_edit_form


class UserEditSchema(SQLAlchemySchemaNode):
    def __init__(self, class_=db.User, includes=None,
                 excludes=None,
                 overrides=None,
                 unknown='ignore', **kw):
        if includes is None:
            includes = ['login', 'vk_id',  'name', 'email', 'active', 'email_checked']
        super().__init__(class_, includes=includes, overrides=overrides, excludes=excludes, unknown=unknown, **kw)
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


class ArticleEditSchema(SQLAlchemySchemaNode):
    def __init__(self, class_=db.Article, includes=None,
                 excludes=None,
                 overrides=None,
                 unknown='ignore', **kw):
        if includes is None:
            includes = ['name', 'system_name',  'path', 'active']
        super().__init__(class_, includes=includes, overrides=overrides, excludes=excludes, unknown=unknown, **kw)
        # code is loaded from article_revision
        self.add(SchemaNode(
            String(),
            name='code',
            title='Html-код статьи',
            # widget=widgets.TextAreaWidget(rows=20, cols=60),
            widget=BootstrapGridEditor(rows=20, cols=60),
        ))
        self.linked_article = None
        self.validator = validate_article_edit_form


class GoodEditSchema(SQLAlchemySchemaNode):
    def __init__(self, class_=db.Good, includes=None,
                 excludes=None,
                 overrides=None,
                 unknown='ignore', **kw):
        if includes is None:
            includes = ['name', 'price', 'is_egood', 'file_path']
        super().__init__(class_, includes=includes, overrides=overrides, excludes=excludes, unknown=unknown, **kw)
        self.linked_good = None
        # self.validator = validate_user_edit_form


# class BuySchema(Schema):
#     email = SchemaNode(
#         String(),
#         title='email',
#         widget=TextInputPlaceholderWidget(
#             placeholder='email'
#         ),
#     )
#
#     password = SchemaNode(
#         String(),
#         title='Пароль',
#         placeholder='*****',
#         widget=PasswordPlaceholderWidget(placeholder='*****'),
#     )

@colander.deferred
def deferred_order_email_widget(node, kw):
    user_logined = kw.get('user_logined', False)
    logout_url = kw.get('logout_url', None)
    return OrderEmailWidget(readonly=user_logined, logout_url=logout_url)


@colander.deferred
def deferred_one_click_buy_captcha_widget(node, kw):
    user_logined = kw.get('user_logined', False)
    if not user_logined and not check_dev_mode():
    # if not user_logined:
        return RecaptchaWidget(lang='ru', theme='clean')
    return widgets.HiddenWidget()


@colander.deferred
def defferred_payment_system_select(node, kw):
    payment_systems = kw.get('payment_systems', [])
    count = len(payment_systems)
    if count > 1:
        return widgets.SelectWidget(values=payment_systems.items())
    elif count == 1:
        return widgets.SelectWidget(values=payment_systems.items(), readonly=True)

    raise Exception('No payment systems available')

# t = get_payment_clients_captions()


class OneClickBuySchema(Schema):
    def __init__(self, typ=colander.Mapping()):
        super().__init__(typ=typ)
        self.add(SchemaNode(
            colander.String(),
            name='email',
            title='Адрес электронной почты',
            validator=colander.Email(),
            widget=deferred_order_email_widget
        ))
        self.add(SchemaNode(
            colander.String(),
            name='captcha',
            title='Капча',
            widget=deferred_one_click_buy_captcha_widget,
            order=1000,
            default='test',
            missing=colander.drop
        ))
        self.add(SchemaNode(
            colander.String(),
            name='payment_system',
            title='Платёжный сервис',
            # validator=colander.Email(),
            widget=defferred_payment_system_select
        ))
        # self.validator = validate_user_edit_form

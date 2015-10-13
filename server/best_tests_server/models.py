import uuid

from hashlib import sha256
from pyramid.security import (
    Allow
)
from sqlalchemy import (
    BigInteger, Column, Integer, Text, Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import ZopeTransactionExtension
import deform.widget
import colander
from dictalchemy import DictableModel
import best_tests_server.helpers as helpers

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(), expire_on_commit=False))
""":type: sqlalchemy.orm.Session """

Base = declarative_base(cls=DictableModel)


ADMIN_GROUP = 'admin'
GROUPS = {ADMIN_GROUP: ['group:admins'],
          None: ['group:users']}


class RootFactory(object):
    __acl__ = [(Allow, 'group:users', 'view'),
               (Allow, 'group:admins', ['view','admin'])]

    def __init__(self, request):
        pass


class TestIndexResult(Base):
    __tablename__ = 'test_index_result'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    test_id = Column(Integer)
    index_id = Column(Integer)


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)


def create_hashed_password(password, salt):
    return sha256(salt.encode() + password.encode()).hexdigest()


def create_salt():
    return uuid.uuid4().hex


def user_login_unique_validator(node, value):
    found = User.by_login(value)
    if found is not None:
        raise colander.Invalid(node, 'Пользователь с таким логином уже существует')


@colander.deferred
def user_login_validator(node, kwargs):
    return colander.All(
        colander.Regex('^[a-z0-9_]+$', 'Логин должен содержать только цифры и английские буквы'),
        user_login_unique_validator,
    )


def email_unique_validator(node, value):
    found = User.by_email(value)
    if found is not None:
        raise colander.Invalid(node, 'Пользователь с таким адресом уже существует')


@colander.deferred
def email_validator(node, kwargs):
    return colander.All(
        colander.Email(),
        email_unique_validator
    )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,
                info={'colanderalchemy': {
                    'title': 'id пользователя'
                }})
    vk_id = Column(BigInteger, unique=True,
                   info={'colanderalchemy': {
                       'title': 'id вконтакте'
                   }})
    login = Column(Text,
                   info={'colanderalchemy': {
                       'title': 'Логин пользователя',
                       'validator': user_login_validator,
                       'missing': colander.required
                   }})
    name = Column(Text,
                  info={'colanderalchemy': {
                      'title': 'Имя пользователя',
                      'missing': None,
                  }})
    email = Column(Text,
                   info={'colanderalchemy': {
                       'title': 'E-mail',
                       'validator': email_validator,
                       'missing': colander.required
                       # 'widget': deform.widget.CheckedInputWidget(
                       #     subject='E-mail',
                       #     confirm_subject='Подтвердите E-mail'
                       # )
                   }})
    group = Column(Text,
                   info={'colanderalchemy': {
                       'title': 'Группа пользователя'
                   }})
    email_check_code = Column(Text)
    email_checked = Column(Boolean, default=False, server_default='false', nullable=False)
    active = Column(Boolean, default=False, server_default='false', nullable=False)
    # stores password hash and salt separated by colon
    password_hash = Column(Text, info={'colanderalchemy': {
                        'title': 'Пароль',
                        'widget': deform.widget.CheckedPasswordWidget(),
                   }})

    def set_password(self, password):
        """thx 2 http://pythoncentral.io/hashing-strings-with-python"""
        salt = create_salt()
        self.password_hash = create_hashed_password(password, salt) + ':' + salt

    def check_password(self, user_password):
        hashed_password_only, salt = self.password_hash.split(':')
        return hashed_password_only == create_hashed_password(user_password, salt)

    @staticmethod
    def get_groups(user_id, request):
        user = User.by_id(user_id)
        """:type user:User"""
        if not user:
            return []
        if user.group not in GROUPS:
            return []
        return GROUPS[user.group]

    @staticmethod
    def by_id(user_id: int):
        """
        :return User
        """
        return DBSession.query(User).filter(User.id == user_id).first()

    @staticmethod
    def by_login(user_login: str):
        """
        :return User
        """
        return DBSession.query(User).filter(User.login == user_login).first()

    @staticmethod
    def by_vk_id(vk_id: int):
        """
        :return User
        """
        return DBSession.query(User).filter(User.vk_id == vk_id).first()

    @staticmethod
    def by_email(email: str):
        """
        :return User
        """
        return DBSession.query(User).filter(User.email == email).first()


    @staticmethod
    def by_any(any):
        """
        :return User
        """
        if isinstance(any, int):
            user = User.by_vk_id(any)
            if user:
                return user
        else:
            user = User.by_login(any)
            if user:
                return user

            user = User.by_email(any)
            if user:
                return user

        return None

    @staticmethod
    def generate_password():
        length = int(helpers.get_setting('generate_password_length', 8))
        return helpers.generate_password(length)

    @staticmethod
    def generate_email_check_code():
        length = int(helpers.get_setting('generate_email_check_code_length', 10))
        return helpers.generate_password(length, True)

    def initiate_email_check(self):
        self.email_check_code = self.generate_email_check_code()
        helpers.send_html_mail(self.email, 'email_check_code',
                               {'email_check_code': self.email_check_code})
        self.email_checked = False
        self.active = False

    def is_admin(self):
        return self.group == ADMIN_GROUP

# TODO коррекция полей перед сохраненинем
# http://docs.sqlalchemy.org/en/latest/orm/events.html ?
# http://docs.sqlalchemy.org/en/latest/orm/session_events.html
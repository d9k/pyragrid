from pyramid.security import (Allow)
from .base import (Base, DBSession, NullableInt)
from sqlalchemy import (
    BigInteger, Column, Integer, Text, Boolean, DateTime, ForeignKey
)
import colander
import sqlalchemy.event
from sqlalchemy.orm import Query
from hashlib import sha256
import uuid
import deform.widget
from .. import helpers

ADMIN_GROUP = 'admin'
GROUPS = {ADMIN_GROUP: ['group:admins'],
          None: ['group:users']}


class RootFactory(object):
    __acl__ = [(Allow, 'group:users', 'view'),
               (Allow, 'group:admins', ['view', 'admin'])]

    def __init__(self, request):
        pass


class User(Base):
    __tablename__ = 'user_'

    id = Column(Integer, primary_key=True,
                info={'colanderalchemy': {
                    'title': 'id пользователя'
                }})
    vk_id = Column(BigInteger,
                   unique=True,
                   nullable=True,
                   info={'colanderalchemy': {
                       'title': 'id вконтакте',
                       # 'widget': deform.widget.TextInputWidget(),
                       # 'missing': colander.drop,
                       # 'missing': colander.null,
                       # 'default': colander.null,
                       'default': None,
                       'typ': NullableInt
                   }})
    login = Column(Text,
                   unique=True,
                   info={'colanderalchemy': {
                       'title': 'Логин пользователя',
                       'validator': colander.Regex(
                               '^[a-z0-9_]+$',
                               'Логин должен содержать только цифры и английские буквы'
                       ),
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
                       'validator': colander.Email(),
                       'missing': colander.required
                       # 'widget': deform.widget.CheckedInputWidget(
                       #     subject='E-mail',
                       #     confirm_subject='Подтвердите E-mail'
                       # )
                   }})
    group_ = Column(Text,
                    info={'colanderalchemy': {
                       'title': 'Группа пользователя'
                   }})
    email_check_code = Column(Text)
    email_checked = Column(Boolean, default=False, server_default='false', nullable=False,
                           info={'colanderalchemy': {
                               'title': 'Почта проверена'
                           }})
    active = Column(Boolean, default=False, server_default='false', nullable=False,
                    info={'colanderalchemy': {
                        'title': 'Аккаунт включен'
                    }})
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
        if self.password_hash is None:
            return False
        hashed_password_only, salt = self.password_hash.split(':')
        return hashed_password_only == create_hashed_password(user_password, salt)

    @staticmethod
    def get_groups(user_id, request):
        user = User.by_id(user_id)
        """:type user:User"""
        if not user:
            return []
        if user.group_ not in GROUPS:
            return []
        return GROUPS[user.group_]

    @staticmethod
    def by_id(user_id: int):
        """
        :return User
        """
        return DBSession.query(User).filter(User.id == user_id).first()

    @staticmethod
    # def by_login(user_login: str, filters=None):
    def by_login(user_login: str, not_id: int = None):
        """
        :return User
        """
        q = DBSession.query(User) \
            .filter(User.login == user_login)
        q = User.filter_not_id(q, not_id)
        return q.first()

    @staticmethod
    def by_vk_id(vk_id: int):
        """
        :return User
        """
        return DBSession.query(User).filter(User.vk_id == vk_id).first()

    @staticmethod
    def by_email(email: str, not_id: int = None):
        """
        :return User
        """
        q = DBSession.query(User).filter(User.email == email)
        q = User.filter_not_id(q, not_id)
        return q.first()

    @staticmethod
    def filter_not_id(query: Query, not_id):
        if not_id is not None:
            return query.filter(User.id != not_id)
        return query

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
        return self.group_ == ADMIN_GROUP

    def before_save(self):
        if not self.name:
            self.name = self.login

    @staticmethod
    def register(self, email, password=None, name=None):
        raise NotImplementedError()
        # return User

# TODO коррекция полей перед сохраненинем
# http://docs.sqlalchemy.org/en/latest/orm/events.html ?
# http://docs.sqlalchemy.org/en/latest/orm/session_events.html


@sqlalchemy.event.listens_for(User, 'before_insert')
def user_before_insert(mapper, connection, user: User):
    user.before_save()


@sqlalchemy.event.listens_for(User, 'before_update')
def user_before_update(mapper, connection, user: User):
    user.before_save()


def create_hashed_password(password, salt):
    return sha256(salt.encode() + password.encode()).hexdigest()


def create_salt():
    return uuid.uuid4().hex

# @colander.deferred
# def email_validator(node, kwargs):
#     return colander.All(
#         colander.Email(),
#         email_unique_validator
#     )

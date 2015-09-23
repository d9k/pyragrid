import uuid

from hashlib import sha256
from pyramid.security import (
    Allow
)
from sqlalchemy import BigInteger, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
""":type: sqlalchemy.orm.Session """

Base = declarative_base()

GROUPS = {'admin': ['group:admins'],
          None: ['group:users']}


class RootFactory(object):
    __acl__ = [(Allow, 'group:users', 'view'),
               (Allow, 'group:admins', 'admin')]

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
                       'title': 'Логин пользователя'
                   }})
    name = Column(Text,
                  info={'colanderalchemy': {
                      'title': 'Имя пользователя'
                  }})
    email = Column(Text,
                   info={'colanderalchemy': {
                       'title': 'E-mail'
                   }})
    group = Column(Text,
                   info={'colanderalchemy': {
                       'title': 'Группа пользователя'
                   }})
    # stores password hash and salt separated by colon
    password_hash = Column(Text, info={'colanderalchemy': {
                        'title': 'Пароль'
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


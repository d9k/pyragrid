import uuid
from sqlalchemy import BigInteger, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from hashlib import sha256
from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
""":type: sqlalchemy.orm.Session """

Base = declarative_base()

GROUPS = {'admin': ['group:admins']}


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

    id = Column(Integer, primary_key=True)
    vk_id = Column(BigInteger, unique=True)
    name = Column(Text)
    group = Column(Text)

    # stores password hash and salt separated by colon
    password_hash = Column(Text)

    def set_password(self, password):
        """thx 2 http://pythoncentral.io/hashing-strings-with-python"""
        salt = create_salt()
        self.password_hash = create_hashed_password(password, salt) + ':' + salt

    def check_password(self, user_password):
        hashed_password_only, salt = self.password_hash.split(':')
        return hashed_password_only == create_hashed_password(user_password, salt)

    @staticmethod
    def get_groups(user_id):
        user = User.by_id(user_id)
        """:type: User"""
        if not user:
            return []
        if user.group not in GROUPS:
            return []
        return GROUPS[user.group]


    @staticmethod
    def by_id(user_id: int):
        """
        :param user_id:int
        :return Test
        """
        return DBSession.query(User).filter(User.id == user_id).first()

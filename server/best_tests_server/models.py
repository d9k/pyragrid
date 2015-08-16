# coding: utf-8
from sqlalchemy import BigInteger, Column, Integer, Text, text, Sequence
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TestIndexResult(Base):
    __tablename__ = 'test_index_result'

    id = Column(Integer, Sequence('test_index_result_id_seq'), primary_key=True)
    user_id = Column(Integer)
    test_id = Column(Integer)
    index_id = Column(Integer)


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, Sequence('tests_id_seq'), primary_key=True)
    name = Column(Text)
    description = Column(Text)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    vk_id = Column(BigInteger)
    name = Column(Text)

# coding: utf-8
from sqlalchemy import BigInteger, Column, Integer, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class TestIndexResult(Base):
    __tablename__ = 'test_index_result'

    id = Column(Integer, primary_key=True, server_default=text("nextval('test_index_result_id_seq'::regclass)"))
    user_id = Column(Integer)
    test_id = Column(Integer)
    index_id = Column(Integer)


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True, server_default=text("nextval('tests_id_seq'::regclass)"))
    name = Column(Text)
    description = Column(Text)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    vk_id = Column(BigInteger)
    name = Column(Text)

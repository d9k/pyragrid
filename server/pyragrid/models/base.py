from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session, sessionmaker, Query, relationship
)
from zope.sqlalchemy import ZopeTransactionExtension
from dictalchemy import DictableModel
import colander
import transaction
from sqlalchemy.exc import DBAPIError

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(), expire_on_commit=False))
""":type: sqlalchemy.orm.Session """

Base = declarative_base(cls=DictableModel)

from colander import null, Invalid


def nullable_int(self, value):
    if value == colander.null or value is None:
        return ''
    else:
        return int(value)


class NullableInt(colander.Number):
    num = nullable_int

def db_save_model(obj):
    try:
        with transaction.manager:
            DBSession.add(obj)
    except DBAPIError as db_api_error:
        return db_api_error
    return None
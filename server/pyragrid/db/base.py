from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session, sessionmaker, Query, relationship
)
from zope.sqlalchemy import ZopeTransactionExtension
from dictalchemy import DictableModel
import colander
import transaction
from sqlalchemy.exc import DBAPIError
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import mapper
import sqlalchemy.event

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


# thx 2 http://stackoverflow.com/a/24893168/1760643
def instant_defaults_listener(target, args, kwargs):
    for key, column in inspect(target.__class__).columns.items():
        if column.default is not None:
            if callable(column.default.arg):
                setattr(target, key, column.default.arg(target))
            else:
                setattr(target, key, column.default.arg)


sqlalchemy.event.listen(mapper, 'init', instant_defaults_listener)

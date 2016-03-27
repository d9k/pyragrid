from sqlalchemy import (
    Column
)
import sqlalchemy
from sqlalchemy import (ForeignKey)
from sqlalchemy.orm import (
    Query, relationship
)
import deform.widget
import colander
from .base import (Base, DBSession, NullableInt)
import datetime

from .enum_money_transaction_status import EnumMoneyTransactionStatus
import sqlalchemy.dialects.postgres as postgres


# TODO research json data type
# TODO http://stackoverflow.com/questions/23878070/using-json-type-with-flask-sqlalchemy-postgresql


class MoneyTransactionStatus(Base):
    __tablename__ = 'money_transaction_status'

    id = Column(
        sqlalchemy.Integer,
        primary_key=True,
        info={'colanderalchemy': {
            'title': 'Id статуса позиции заказа',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    money_transaction_id = Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('order_good.id'),
        info={'colanderalchemy': {
            'title': 'Заказанный товар',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    provider = Column(
        sqlalchemy.Text,
        info={'colanderalchemy': {
            'title': 'Платёжный сервис',
        }})

    status = Column(
        sqlalchemy.Enum(
            *EnumMoneyTransactionStatus.get_values(),
            name='enum_order_status',
            native_enum=False
        ),
        # TODO readonly select
        info={'colanderalchemy': {
            'title': 'Состояние',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    request_data = Column(
        postgres.JSON,
        info={'colanderalchemy': {
            'title': 'Данные запроса',
            'widget': deform.widget.DateTimeInputWidget(readonly=True)
        }})

    answer_data = Column(
        postgres.JSON,
        info={'colanderalchemy': {
            'title': 'Данные ответа',
            'widget': deform.widget.DateTimeInputWidget(readonly=True)
        }})

    error = Column(
        postgres.JSON,
        info={'colanderalchemy': {
            'title': 'Данные ответа',
            'widget': deform.widget.DateTimeInputWidget(readonly=True)
        }})

    user_id = Column(
        sqlalchemy.Integer,
        ForeignKey('user_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})


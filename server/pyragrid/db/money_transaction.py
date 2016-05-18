from sqlalchemy import (
    Column, ForeignKey
)
import sqlalchemy
import deform.widget
import colander
from .base import (Base, DBSession, NullableInt)
from sqlalchemy.orm import (
    Query, relationship
)
# from .enum_order_good_status import EnumOrderGoodStatus
from .enum_money_transaction_status import EnumMoneyTransactionStatus
from .enum_money_transaction_type import EnumMoneyTransactionType


class MoneyTransaction(Base):

    __tablename__ = 'money_transaction'

    id = Column(
        sqlalchemy.Integer,
        primary_key=True,
        info={'colanderalchemy': {
            'title': 'Id транзакции',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }}
    )

    order_id = Column(
        sqlalchemy.Integer,
        ForeignKey('user_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    status = Column(
        sqlalchemy.Enum(
            *EnumMoneyTransactionStatus.get_values(),
            name='enum_money_transaction_status',
            native_enum=False
        ),
        default=EnumMoneyTransactionStatus.init_request_sent,
        info={'colanderalchemy': {
            'title': 'Состояние транзации',
            # TODO readonly select widget
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    type = Column(
        sqlalchemy.Enum(
            *EnumMoneyTransactionType.get_values(),
            name='enum_money_transaction_type',
            native_enum=False
        ),
        default=EnumMoneyTransactionType.buy,
        info={'colanderalchemy': {
            'title': 'Тип транзакции',
            # TODO readonly select widget
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    user_id = Column(
        sqlalchemy.Integer,
        ForeignKey('user_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

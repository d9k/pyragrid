from sqlalchemy import (
    Column
)
import sqlalchemy
import deform.widget
import colander
from .base import (Base, DBSession, NullableInt)
from sqlalchemy.orm import (
    Query, relationship
)
from .enum import (SimpleEnum)


class EnumOrderGoodStatus(SimpleEnum):
    created = '', 'Создан'
    payment_began = '', 'Оплпата начата'
    payment_failed = '', 'Неуспешная оплата'
    paid = '', 'Оплачен'
    refund_began = '', 'Возврат средств'
    refund_failed = '', 'Неуспешный возврат'
    refunded = '', 'Средства возвращены'


class OrderGood(Base):
    __tablename__ = 'order_good'

    id = Column(
        sqlalchemy.Integer,
        primary_key=True,
        info={'colanderalchemy': {
            'title': 'Id заказа',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }}
    )

    status = Column(
        sqlalchemy.Enum(
            *EnumOrderGoodStatus.get_values(),
            name='EnumOrderState',
            native_enum=False
        ),
        default=EnumOrderGoodStatus.created,
        info={'colanderalchemy': {
            'title': 'Состояние заказа',
            # TODO readonly select widget
            'widget': deform.widget.TextInputWidget(readonly=True)
        }}
    )

    count = Column(
        sqlalchemy.Float(2),
        default=1,
        info={'colanderalchemy': {
           'title': 'Общая сумма заказа',
           'widget': deform.widget.TextInputWidget(readonly=True)
        }}
    )

    total = Column(
        sqlalchemy.Float(2),
        info={'colanderalchemy': {
            'title': 'Общая сумма заказа',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }}
    )

    paid_amount = Column(
        sqlalchemy.Float(2),
        info={'colanderalchemy': {
            'title': 'Оплаченная сумма',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }}
    )

    refund_amount = Column(
        sqlalchemy.Float(2),
        info={'colanderalchemy': {
            'title': 'Сумма возврата',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }}
    )

    user_id = Column(
        sqlalchemy.Integer,
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }}
    )


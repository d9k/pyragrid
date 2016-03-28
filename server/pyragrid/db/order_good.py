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
from .enum_order_good_status import EnumOrderGoodStatus


class OrderGood(Base):

    __tablename__ = 'order_good'

    id = Column(
        sqlalchemy.Integer,
        primary_key=True,
        info={'colanderalchemy': {
            'title': 'Id заказанного товара',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }}
    )

    order_id = Column(
        sqlalchemy.Integer,
        ForeignKey('order_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    good_id = Column(
        sqlalchemy.Integer,
        ForeignKey('good.id'),
        info={'colanderalchemy': {
            'title': 'Товар',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    status = Column(
        sqlalchemy.Enum(
            *EnumOrderGoodStatus.get_values(),
            name='enum_order_status',
            native_enum=False
        ),
        default=EnumOrderGoodStatus.created,
        info={'colanderalchemy': {
            'title': 'Состояние заказанного товара',
            # TODO readonly select widget
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    count = Column(
        sqlalchemy.Numeric(12, 4),
        default=1,
        info={'colanderalchemy': {
           'title': 'Количество заказанного товара',
           'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    total = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Сумма заказанного товара',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }} )

    paid_amount = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Оплаченная сумма',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    refund_count = Column(
        sqlalchemy.Numeric(12, 4),
        default=0,
        info={'colanderalchemy': {
            'title': 'Количество возвращённого товара',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    refund_amount = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Возвращённая сумма',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    user_id = Column(
        sqlalchemy.Integer,
        ForeignKey('user_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

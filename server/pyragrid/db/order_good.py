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
from .enum_order_good_status import EnumOrderGoodStatus



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

    # TODO or not TODO? redundant data
    status = Column(
        sqlalchemy.Enum(
            *EnumOrderGoodStatus.get_values(),
            name='EnumOrderStatus',
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
            'title': 'Возвращённая сумма',
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


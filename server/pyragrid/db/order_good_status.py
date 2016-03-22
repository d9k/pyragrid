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

from .enum_order_good_status import EnumOrderGoodStatus


class OrderGoodStatus(Base):
    __tablename__ = 'order_good_status'

    id = Column(
        sqlalchemy.Integer,
        primary_key=True,
        info={'colanderalchemy': {
            'title': 'Id статуса позиции заказа',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    order_good_id = Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('order_good.id'),
        info={'colanderalchemy': {
            'title': 'Заказ',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    datetime = Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False,
        info={'colanderalchemy': {
            'title': 'Время',
            'widget': deform.widget.DateTimeInputWidget(readonly=True)
        }})

    status = Column(
        sqlalchemy.Enum(
            *EnumOrderGoodStatus.get_values(),
            name='enum_order_status',
            native_enum=False
        ),
        # TODO readonly select
        info={'colanderalchemy': {
            'title': 'Состояние',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    paid = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
          'title': 'Оплачено',
          'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    rejected = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Возврат',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    shop_money_delta = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Изменение счёта магазина',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }}
    )

    user_id = Column(
        sqlalchemy.Integer,
        ForeignKey('user_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})


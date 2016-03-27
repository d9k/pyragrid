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


class RefundOrderGood(Base):
    __tablename__ = 'refund_order_good'

    id = Column(
        sqlalchemy.Integer,
        primary_key=True,
        info={'colanderalchemy': {
            'title': 'Id возврата позиции заказа',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    refund_id = Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('order_good.id'),
        info={'colanderalchemy': {
            'title': 'Возврат',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    order_good_id = Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('order_good.id'),
        info={'colanderalchemy': {
            'title': 'Заказанный товар',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    count = Column(
        sqlalchemy.Numeric(12, 4),
        default=1,
        info={'colanderalchemy': {
            'title': 'Количество возвращаемого товара',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    total = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Сумма возвращаемого товара',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    status = Column(
        sqlalchemy.Enum(
            *EnumOrderGoodStatus.get_values(),
            name='enum_order_status',
            native_enum=False
        ),
        # TODO readonly select
        info={'colanderalchemy': {
            'title': 'Состояние возврата товара',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    user_id = Column(
        sqlalchemy.Integer,
        ForeignKey('user_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})


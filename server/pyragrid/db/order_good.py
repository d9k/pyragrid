from sqlalchemy import (
    Column, ForeignKey
)
import sqlalchemy
import deform.widget
import colander
from .base import (Base, DBSession, NullableInt)
from .order_good_status import OrderGoodStatus
from sqlalchemy.orm import (
    Query, relationship
)
from .enum_order_good_status import EnumOrderGoodStatus


class OrderGood(Base):
    """`OrderGood` is specified by `order_id`, `good_id` and `price` (`price` be may changed after purchase of good so `price` must pe stored at `OrderGood` to calculate refund sum properly).
    """

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
        default=EnumOrderGoodStatus.wanted_add,
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

    price = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Стоимость заказанного товара',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    wanted_total = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Сумма заказанного товара',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

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

    good = relationship('Good')
    order = relationship('Order', back_populates='order_goods')
    user = relationship('User')
    statuses = relationship('OrderGoodStatus', back_populates='orderGood')

    def reload_price(self):
        self.price = self.good.price

    def count_wanted_total(self, reload_price=False):
        if reload_price:
            self.reload_price()
        self.wanted_total = float(self.price) * float(self.count)

    def create_status(self, status=EnumOrderGoodStatus.wanted_add):
        DBSession.flush()
        self.statuses.append(OrderGoodStatus(status=status, count=self.count))

    def add_count(self, count):
        self.count += count
        # TODO ! create order_good_status model
        self.create_status()
        self.count_wanted_total(True)


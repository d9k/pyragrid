import deform.widget
import sqlalchemy
from sqlalchemy import (
    Column, ForeignKey
)
from .base import (Base, DBSession)
from sqlalchemy.orm import (
    Query, relationship
)
from .order_good import OrderGood
from .good import Good


class Order(Base):
    __tablename__ = 'order_'

    id = Column(
        sqlalchemy.Integer,
        primary_key=True,
        info={'colanderalchemy': {
            'title': 'Id заказа',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})
    # state = Column(sqlalchemy.Enum(*EnumOrderState.get_values(), name='EnumOrderState', native_enum=False),
    #                # TODO readonly select
    #             info={'colanderalchemy': {
    #                 'title': 'Состояние заказа',
    #                 'widget': deform.widget.TextInputWidget(readonly=True)
    #             }}
    #                )
    # TODO state as enum http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/
    total = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Общая сумма заказа',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    paid_amount = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Оплачено',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    rejected_amount = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Сумма возврата',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    user_id = Column(
        sqlalchemy.Integer,
        ForeignKey('user_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    # relations
    order_goods = relationship('OrderGood', back_populates='order')
    """
    :type OrderGood[]
    """
    # TODO how to doc type?

    @staticmethod
    def by_id(id_: int):
        """
        :return Order
        """
        return DBSession.query(Order).filter(Order.id == id_).first()

    def recount_total(self):
        """
        :var order_good: OrderGood
        """
        total = 0
        # what if price changed?
        for order_good in self.order_goods:
            total += order_good.total
        self.total = total

    def find_order_good(self, good_id):
        for order_good in self.order_goods:
            if order_good.good_id == good_id:
                return order_good
        good = Good.by_id(good_id)
        new_order_good = OrderGood(good_id=good.id, count=0, user_id=self.user_id)
        self.order_goods.append(new_order_good)
        DBSession.flush()
        return new_order_good

    def add_good(self, good_id, count=1.0):
        order_good = self.find_order_good(good_id)
        order_good.add_count(count)
        self.recount_total()

    def remove_good(self, order_good_id):
        raise NotImplementedError()

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
from .enum_order_status import EnumOrderStatus
from .enum_order_good_status import EnumOrderGoodStatus
from .money_transaction import MoneyTransaction
from .money_transaction_status import MoneyTransactionStatus
from typing import Union


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
    wanted_total = Column(
        sqlalchemy.Numeric(12, 2),
        default=0.0,
        info={'colanderalchemy': {
            'title': 'Общая сумма заказа',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    paid_amount = Column(
        sqlalchemy.Numeric(12, 2),
        default=0.0,
        info={'colanderalchemy': {
            'title': 'Оплачено',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    refund_amount = Column(
        sqlalchemy.Numeric(12, 2),
        default=0.0,
        info={'colanderalchemy': {
            'title': 'Сумма возврата',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    status = Column(
        sqlalchemy.Enum(
            *EnumOrderStatus.get_values(),
            name='enum_order_status',
            native_enum=False
        ),
        nullable=False,
        default=EnumOrderStatus.cart,
        # TODO readonly select
        info={'colanderalchemy': {
            'title': 'Состояние',
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

    def recount_wanted_total(self):
        """
        :var order_good: OrderGood
        """
        self.wanted_total = sum([order_good.wanted_total for order_good in self.order_goods])

    def recount_refund_amount(self):
        self.refund_amount = sum([order_good.refund_amount for order_good in self.order_goods])

    def recount_paid_amount(self):
        self.paid_amount = sum([order_good.paid_amount for order_good in self.order_goods])

    def recount_totals(self):
        self.recount_wanted_total()
        self.recount_refund_amount()
        self.recount_paid_amount()

    def get_order_good(self, good_id, price=None):
        for order_good in self.order_goods:
            if order_good.good_id == good_id:
                if price == order_good.price:
                    return order_good
        # not found, creating new
        good = Good.by_id(good_id)
        new_order_good = OrderGood(good_id=good.id, user_id=self.user_id)
        self.order_goods.append(new_order_good)
        DBSession.flush()
        new_order_good.set_price()
        return new_order_good

    def alter_wanted_good_count(self, good_id, delta_count=1.0, price=None):
        order_good = self.get_order_good(good_id, price)
        order_good.alter_count(delta_count)
        self.recount_wanted_total()

    def remove_good(self, order_good_id):
        raise NotImplementedError()

    def get_amount_to_pay(self):
        return self.wanted_total + self.refund_amount - self.paid_amount

    @staticmethod
    def to_order_status(order_good_status: str):
        status_match = {
            EnumOrderGoodStatus.payment_began: EnumOrderStatus.payment_began,
            EnumOrderGoodStatus.paid: EnumOrderStatus.paid,
            EnumOrderGoodStatus.payment_failed: EnumOrderStatus.payment_failed,
        }
        return status_match.get(order_good_status)

    def append_goods_status(self, status: str, transaction: Union[int, MoneyTransaction]=None,
                            # transaction_status: Union[int, MoneyTransactionStatus]=None
                            ):
        for order_good in self.order_goods:
            """:type order_good OrderGood"""
            order_good.append_status(status, transaction)
        self_new_status = self.to_order_status(status)
        if self_new_status is not None:
            self.status = self_new_status


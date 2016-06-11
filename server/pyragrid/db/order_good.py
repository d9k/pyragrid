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
from sqlalchemy import UniqueConstraint
from .enum_order_good_status import EnumOrderGoodStatus
from typing import (Union, Optional)
from .money_transaction_status import MoneyTransactionStatus
from .money_transaction import MoneyTransaction


class OrderGood(Base):
    """`OrderGood` is specified by `order_id`, `good_id` and `price` (`price` be may changed after purchase of good so `price` must pe stored at `OrderGood` to calculate refund sum properly).
    """

    __tablename__ = 'order_good'
    __table_args__ = (
        UniqueConstraint('order_id', 'good_id', 'price', name='order_good_unique'),
    )

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

    wanted_count = Column(
        sqlalchemy.Numeric(12, 4),
        default=0,
        info={'colanderalchemy': {
           'title': 'Количество заказанного товара',
           'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    # status = Column(
    #     sqlalchemy.Enum(
    #         *EnumOrderGoodStatus.get_values(),
    #         name='enum_order_status',
    #         native_enum=False
    #     ),
    #     default=EnumOrderGoodStatus.wanted_alter,
    #     info={'colanderalchemy': {
    #         'title': 'Состояние заказанного товара',
    #         # TODO readonly select widget
    #         'widget': deform.widget.TextInputWidget(readonly=True)
    #     }})

    price = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Стоимость заказанного товара',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    wanted_total = Column(
        sqlalchemy.Numeric(12, 2),
        default=0.0,
        info={'colanderalchemy': {
            'title': 'Сумма заказанного товара',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    paid_amount = Column(
        sqlalchemy.Numeric(12, 2),
        default=0.0,
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
        default=0,
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
    """:type statuses list of OrderGoodStatus"""

    def set_price(self):
        self.price = self.good.price

    def count_wanted_total(self):
        self.wanted_total = float(self.price) * float(self.wanted_count)

    def alter_count(self, delta_count):
        self.wanted_count += delta_count
        # TODO ! create order_good_status model
        DBSession.flush()
        self.statuses.append(OrderGoodStatus(status=EnumOrderGoodStatus.wanted_alter, count=delta_count))
        self.count_wanted_total()

    def recount_wanted_total(self):
        self.wanted_count = sum([
            _status.count for _status in self.statuses
            if _status.status == EnumOrderGoodStatus.wanted_alter
        ])
        self.count_wanted_total()

    def recount_refund_amount(self):
        self.refund_amount = sum([
            _status.count for _status in self.statuses
            if _status.status == EnumOrderGoodStatus.refunded
        ])

    def recount_paid_amount(self):
        self.paid_amount = sum([
            _status.count for _status in self.statuses
            if _status.status == EnumOrderGoodStatus.paid
        ])

    def recount_totals(self):
        self.recount_wanted_total()
        self.recount_refund_amount()
        self.recount_paid_amount()

    def get_amount_to_pay(self):
        return self.wanted_total - self.paid_amount + self.refund_amount

    def get_amount_to_refund(self):
        return self.paid_amount - self.refund_amount

    def get_statuses(self, status: str, transaction: Union[int, MoneyTransaction, None]=None):
        transaction = MoneyTransaction.ensure_object(transaction)
        return [
            order_good_status for order_good_status in self.statuses
            if order_good_status.status == status and
            (transaction is None or order_good_status.transaction == transaction)
        ]

    def append_status(self, status: str, transaction: Union[int, MoneyTransaction],
                      # transaction_status: Union[int, MoneyTransactionStatus]
                      ):

        transaction = MoneyTransaction.ensure_object(transaction)
        """:type transaction MoneyTransaction"""
        # transaction_status = MoneyTransaction.ensure_object(transaction_status)
        transaction_status = transaction.get_status()
        count = None

        if status == EnumOrderGoodStatus.payment_began:
            self.recount_wanted_total()
            count = self.wanted_count
        elif status in [EnumOrderGoodStatus.paid, EnumOrderGoodStatus.payment_failed]:
            payment_began_statuses = self.get_statuses(EnumOrderGoodStatus.payment_began, transaction)  # TODO what if int?
            if len(payment_began_statuses) != 1:
                raise Exception('unexpected statuses count error')
            payment_began_status = payment_began_statuses[0]
            count = payment_began_status.count

        self.statuses.append(OrderGoodStatus(
            status=status,
            count=count,
            transaction=transaction,
            transaction_status=transaction_status
        ))

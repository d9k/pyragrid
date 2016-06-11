from sqlalchemy import (
    Column, ForeignKey
)
from .money_transaction_status import MoneyTransactionStatus
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
from . import order_good_status
from . import order as order_
from . import money_transaction_status
from typing import (Union, Optional)


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
        ForeignKey('order_.id'),
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

    payment_system = Column(
        sqlalchemy.String(20),
        nullable=False,
        info={'colanderalchemy': {
            'title': 'Платёжная система',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    shop_money_delta = Column(
        sqlalchemy.Numeric(12, 2),
        default=0.0,
        nullable=False,
        info={'colanderalchemy': {
            'title': 'Изменение средств магазина (в случае успеха)',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    user_id = Column(
        sqlalchemy.Integer,
        ForeignKey('user_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    order = relationship('Order')  # , back_populates='money_transactions')
    user = relationship('User')
    statuses = relationship('MoneyTransactionStatus', back_populates='money_transaction')

    @classmethod
    def by_id(cls, id_: int):
        """:return MoneyTransaction"""
        return DBSession.query(cls).filter(cls.id == id_).first()

    @classmethod
    def ensure_object(cls, something):
        """
        :arg something Union[int, MoneyTransaction]
        :return Optional[MoneyTransaction]
        """
        if type(something) is int:
            id_ = something
            something = cls.by_id(id_)
        return something

    def status_append(self, new_status: MoneyTransactionStatus):
        self.statuses.append(new_status)
        self.status = new_status.status

    def get_status(self, status: Optional[str]=None) -> Optional[money_transaction_status.MoneyTransactionStatus]:

        if status is None:
            status = self.status

        for transaction_status in self.statuses:
            """:type transaction_status money_transaction_status.MoneyTransactionStatus"""
            if transaction_status.status == status:
                return transaction_status
        return None

    # """:type order order_.Order"""

    # def init(self):
    #     new_status = MoneyTransactionStatus(money_transaction_id=self.id)
    #     self.statuses.append(new_status)
    #     new_status.build_form()
    #     return new_status


import deform.widget
import sqlalchemy
from sqlalchemy import (
    Column, ForeignKey
)
from .base import (Base, DBSession)
from sqlalchemy.orm import (
    Query, relationship
)


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

    @staticmethod
    def by_id(id_: int):
        """
        :return Article
        """
        return DBSession.query(Order).filter(Order.id == id_).first()

    def recount_sum(self):
        raise NotImplementedError()

    def add_good(self, good_id, count=1.0):
        raise NotImplementedError()
        # self.recount_sum()

    def remove_good(self, order_good_id):
        raise NotImplementedError()

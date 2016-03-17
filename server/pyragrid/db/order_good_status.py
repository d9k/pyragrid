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


class OrderGoodStatus(Base):
    __tablename__ = 'orders_goods_statuses'

    id = Column(sqlalchemy.Integer, primary_key=True,
                info={'colanderalchemy': {
                    'title': 'Id позиции заказа',
                    # 'widget': deform.widget.TextInputWidget(readonly=True)
                }})
    status = Column(sqlalchemy.Enum(*EnumOrderGoodStatus.get_values(), name='EnumOrderStatus', native_enum=False),
                # TODO readonly select
                info={'colanderalchemy': {
                    'title': 'Состояние',
                    'widget': deform.widget.TextInputWidget(readonly=True)
                }}
                )

    paid = Column(sqlalchemy.Float(2),
                  info={'colanderalchemy': {
                      'title': 'Оплачено',
                      'widget': deform.widget.TextInputWidget(readonly=True)
                  }}
                  )

    rejected = Column(sqlalchemy.Float(2),
                      info={'colanderalchemy': {
                          'title': 'Возврат',
                          'widget': deform.widget.TextInputWidget(readonly=True)
                      }}
                      )

    user_id = Column(sqlalchemy.Integer,
                    info={'colanderalchemy': {
                        'title': 'Пользователь',
                        'widget': deform.widget.TextInputWidget(readonly=True)
                    }}
                    )


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
from .enum import (SimpleEnum)


class EnumOrderGoodState(SimpleEnum):
    created = '', 'Создан'
    rejected = '', 'Отменён'
    paid = '', 'Оплачен'


class OrderGood(Base):
    __tablename__ = 'OrderGood'

    id = Column(sqlalchemy.Integer, primary_key=True,
                info={'colanderalchemy': {
                    'title': 'Id заказа',
                    # 'widget': deform.widget.TextInputWidget(readonly=True)
                }})
    state = Column(sqlalchemy.Enum(*EnumOrderGoodState.get_values(), name='EnumOrderState', native_enum=False),
                # TODO readonly select
                info={'colanderalchemy': {
                    'title': 'Состояние заказа',
                    'widget': deform.widget.TextInputWidget(readonly=True)
                }}
                )
    # TODO state as enum http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/
    total = Column(sqlalchemy.Float(2),
                   info={'colanderalchemy': {
                    'title': 'Общая сумма заказа',
                    'widget': deform.widget.TextInputWidget(readonly=True)
                    }}
                   )

    paid = Column(sqlalchemy.Float(2),
                  info={'colanderalchemy': {
                      'title': 'Оплаченная сумма',
                      'widget': deform.widget.TextInputWidget(readonly=True)
                  }}
                  )

    rejected = Column(sqlalchemy.Float(2),
                      info={'colanderalchemy': {
                          'title': 'Сумма возврата',
                          'widget': deform.widget.TextInputWidget(readonly=True)
                      }}
                      )

    userId = Column(sqlalchemy.Integer,
                    info={'colanderalchemy': {
                        'title': 'Пользователь',
                        'widget': deform.widget.TextInputWidget(readonly=True)
                    }}
                    )


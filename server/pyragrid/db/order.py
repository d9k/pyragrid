import deform.widget
import sqlalchemy
from sqlalchemy import (
    Column
)
from .base import (Base)
from .enum import (SimpleEnum)


class EnumOrderState(SimpleEnum):
    created = '', 'Создан'
    rejected = '', 'Отменён'
    paid = '', 'Оплачен'


class Order(Base):
    __tablename__ = 'order'

    id = Column(sqlalchemy.Integer, primary_key=True,
                info={'colanderalchemy': {
                    'title': 'Id заказа',
                    # 'widget': deform.widget.TextInputWidget(readonly=True)
                }})
    state = Column(sqlalchemy.Enum(*EnumOrderState.get_values(), name='EnumOrderState', native_enum=False),
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

    userId = Column(sqlalchemy.Integer,
                    info={'colanderalchemy': {
                        'title': 'Пользователь',
                        'widget': deform.widget.TextInputWidget(readonly=True)
                    }}
                    )

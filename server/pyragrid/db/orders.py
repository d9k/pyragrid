from sqlalchemy import (
    Column, Integer, Text, Boolean, DateTime, ForeignKey
)
import sqlalchemy
import deform.widget
import colander
from .base import (Base, DBSession, NullableInt)
from sqlalchemy.orm import (
    Query, relationship
)
from .enum import (DeclEnum)

class EnumOrderState(DeclEnum):
    created = "created", "Создан"
    rejected = "rejected", "Отменён"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True,
                info={'colanderalchemy': {
                    'title': 'id заказа',
                    'widget': deform.widget.TextInputWidget(readonly=True)
                }})
    state = Column(EnumOrderState.db_type(), primary_key=True,
                # info={'colanderalchemy': {
                #     'title': 'id заказа',
                #     'widget': deform.widget.TextInputWidget(readonly=True)
                # }}
                )
    # TODO state as enum http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/
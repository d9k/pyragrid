import deform.widget
import sqlalchemy
from sqlalchemy import (
    Column, ForeignKey
)
from .base import (Base)
from .enum_refund_status import EnumRefundStatus


class Refund(Base):
    __tablename__ = 'refund'

    id = Column(
        sqlalchemy.Integer,
        primary_key=True,
        info={'colanderalchemy': {
            'title': 'Id возврата',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    order_id = Column(
        sqlalchemy.Integer,
        ForeignKey('order.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    total = Column(
        sqlalchemy.Numeric(12, 2),
        info={'colanderalchemy': {
            'title': 'Общая сумма возврата',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    status = Column(
        sqlalchemy.Enum(
            *EnumRefundStatus.get_values(),
            name='enum_refund_status',
            native_enum=False
        ),
        default=EnumRefundStatus.created,
        info={'colanderalchemy': {
            'title': 'Состояние заказа',
            # TODO readonly select widget
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    # datetime = Column(
    #     sqlalchemy.DateTime,
    #     default=datetime.datetime.utcnow,
    #     nullable=False,
    #     info={'colanderalchemy': {
    #         'title': 'Время',
    #         'widget': deform.widget.DateTimeInputWidget(readonly=True)
    #     }})

    reason = Column(
        sqlalchemy.Text,
        info={'colanderalchemy': {
            'title': 'Код статьи',
            'widget': deform.widget.TextAreaWidget()
        }})

    user_id = Column(
        sqlalchemy.Integer,
        ForeignKey('user_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})
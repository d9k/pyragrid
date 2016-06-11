from sqlalchemy import (
    Column
)
import sqlalchemy
from sqlalchemy import (ForeignKey)
from sqlalchemy.orm import (
    Query, relationship
)
import deform.widget
import colander
from .base import (Base, DBSession, NullableInt)
import datetime

from .enum_money_transaction_status import EnumMoneyTransactionStatus
from .enum_request_method import EnumRequestMethod
import sqlalchemy.dialects.postgres as postgres
import dominate
import dominate.tags as tag


# TODO research json data type
# TODO http://stackoverflow.com/questions/23878070/using-json-type-with-flask-sqlalchemy-postgresql


class MoneyTransactionStatus(Base):
    __tablename__ = 'money_transaction_status'

    id = Column(
        sqlalchemy.Integer,
        primary_key=True,
        info={'colanderalchemy': {
            'title': 'Id статуса позиции заказа',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    money_transaction_id = Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('money_transaction.id'),
        info={'colanderalchemy': {
            'title': 'Заказанный товар',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    status = Column(
        sqlalchemy.Enum(
            *EnumMoneyTransactionStatus.get_values(),
            name='enum_order_status',
            native_enum=False
        ),
        default=EnumMoneyTransactionStatus.init_request_sent,
        # TODO readonly select
        info={'colanderalchemy': {
            'title': 'Состояние',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    request_data = Column(
        postgres.JSON,
        default={},
        info={'colanderalchemy': {
            'title': 'Данные запроса',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    url = Column(
        sqlalchemy.Text(),
        info={'colanderalchemy': {
            'title': 'URL запроса',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    request_method = Column(
        sqlalchemy.Enum(
            *EnumRequestMethod.get_values(),
            name='enum_request_method',
            native_enum=False
        ),
        default=EnumRequestMethod.GET,
        nullable=False,
        info={'colanderalchemy': {
            'title': 'метод запроса',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    additional_data = Column(
        postgres.JSON,
        default={},
        info={'colanderalchemy': {
            'title': 'Дополнительные данные',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    answer_data = Column(
        postgres.JSON,
        default={},
        info={'colanderalchemy': {
            'title': 'Данные ответа',
            'widget': deform.widget.DateTimeInputWidget(readonly=True)
        }})

    error = Column(
        postgres.JSON,
        default={},
        info={'colanderalchemy': {
            'title': 'Данные ответа',
            'widget': deform.widget.DateTimeInputWidget(readonly=True)
        }})

    user_id = Column(
        sqlalchemy.Integer,
        ForeignKey('user_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    def render_post_form(self, auto_redirect=False):
        form = tag.form(id='payment_redirect_form', action=self.url, method=self.request_method)
        with form:
            for name, value in self.request_data.items():
                tag.input(type='hidden', name=name, value=value)
            tag.input(type='submit', name='submit', value='Продолжить оплату')
        return form.render()

    money_transaction = relationship('MoneyTransaction', back_populates='statuses')
    user = relationship('User')


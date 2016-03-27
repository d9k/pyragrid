from sqlalchemy import (
    Column
)
import sqlalchemy
from sqlalchemy import (ForeignKey)
from sqlalchemy.orm import (
    Query, relationship
)
import deform.widget
from .base import (Base, DBSession, NullableInt)
import datetime

from .enum_order_good_status import EnumOrderGoodStatus


class EgoodDownloadLink(Base):
    __tablename__ = 'egood_download_link'

    id = Column(
        sqlalchemy.Integer,
        primary_key=True,
        info={'colanderalchemy': {
            'title': 'Id ссылки на скачивание',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    egood_id = Column(
        sqlalchemy.Integer,
        ForeignKey('good.id'),
        info={'colanderalchemy': {
            'title': 'Электронный товар',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    download_code = Column(
        sqlalchemy.Text, default=True, server_default='true',
        nullable=False,
        info={'colanderalchemy': {
            'title': 'Ссылка активна',
        }})

    for_user_id = Column(
        sqlalchemy.Integer,
        ForeignKey('user_.id'),
        info={'colanderalchemy': {
            'title': 'Пользователь',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})\

    created_at = Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False,
        info={'colanderalchemy': {
            'title': 'Время',
            'widget': deform.widget.DateTimeInputWidget(readonly=True)
        }})

    expires = Column(
        sqlalchemy.DateTime,
        # TODO + 1 week
        default=datetime.datetime.utcnow,
        nullable=False,
        info={'colanderalchemy': {
            'title': 'Истекает',
            'widget': deform.widget.DateTimeInputWidget(readonly=True)
        }})

    downloads_count = Column(
        sqlalchemy.Integer, default=0,
        info={'colanderalchemy': {
            'title': 'Количество скачиваний',
            # 'widget': deform.widget.TextInputWidget(readonly=True)
        }})



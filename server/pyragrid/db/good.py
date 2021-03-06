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
from pyragrid import widgets
# deform.widget.TextInputWidget(readonly=True)


class Good(Base):
    __tablename__ = 'good'

    id = Column(
        Integer, primary_key=True,
        info={'colanderalchemy': {
            'title': 'id товара',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    name = Column(
        Text,
        nullable=False,
        unique=True,
        info={'colanderalchemy': {
          'title': 'Название товара',
          # 'missing': None,
        }})

    price = Column(
        sqlalchemy.Numeric(12, 2), default=10.0,
        info={'colanderalchemy': {
            'title': 'Цена',
            'missing': 0,
        }}
        )

    is_egood = Column(
        Boolean, default=False, server_default='false',
        nullable=False,
        info={'colanderalchemy': {
            'title': 'Это электронный товар',
        }})

    # TODO rename to file_path
    file_path = Column(
        Text,
        info={'colanderalchemy': {
            'title': 'Путь к файлу',
            'widget': widgets.FileDialog()
            # TODO file select field, translate to relative path
        }})

    active = Column(
        Boolean, default=False, server_default='false', nullable=False,
        info={'colanderalchemy': {
            'title': 'Товар включен'
        }})

    # downloadLinkBegin = Column(Text,
    #         info={'colanderalchemy': {
    #             'title': 'Путь к файлу',
    #             # TODO file select field, translate to relative path
    #         }}
    # )

    # relations
    # revisions = relationship('ArticleRevision', back_populates='article')

    @staticmethod
    def by_id(id_: int):
        """
        :return Article
        """
        return DBSession.query(Good).filter(Good.id == id_).first()

    @staticmethod
    def filter_not_id(query: Query, not_id):
        if not_id is not None:
            return query.filter(Good.id != not_id)
        return query

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


class Good(Base):
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True,
                info={'colanderalchemy': {
                    'title': 'id товара',
                    'widget': deform.widget.TextInputWidget(readonly=True)
                }})
    name = Column(Text,
                  unique=True,
                  info={'colanderalchemy': {
                      'title': 'Название товара',
                      # 'missing': None,
                  }})
    price = Column(sqlalchemy.Numeric(12, 2),
                   info={'colanderalchemy': {
                       'title': 'Цена',
                       # 'missing': None,
                   }}
                   )
    isEgood = Column(Boolean, default=False, server_default='false',
                        nullable=False,
                        info={'colanderalchemy': {
                            'title': 'Это электронный товар',
                        }})

    filePath = Column(Text,
            info={'colanderalchemy': {
                'title': 'Путь к файлу',
                # TODO file select field, translate to relative path
            }}
    )

    # downloadLinkBegin = Column(Text,
    #         info={'colanderalchemy': {
    #             'title': 'Путь к файлу',
    #             # TODO file select field, translate to relative path
    #         }}
    # )

    # relations
    # revisions = relationship('ArticleRevision', back_populates='article')

    @staticmethod
    def by_id(id: int):
        """
        :return Article
        """
        return DBSession.query(Good).filter(Good.id == id).first()

    @staticmethod
    def filter_not_id(query: Query, not_id):
        if not_id is not None:
            return query.filter(Good.id != not_id)
        return query

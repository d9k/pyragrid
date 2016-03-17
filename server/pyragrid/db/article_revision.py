from sqlalchemy import (
    BigInteger, Column, Integer, Text, Boolean, DateTime, ForeignKey
)
from .base import (Base, DBSession, NullableInt)
import deform.widget
import datetime
from sqlalchemy.orm import (relationship)


class ArticleRevision(Base):

    __tablename__ = 'article_revision'

    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {
            'title': 'глобальный id ревизии',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    articleId = Column(
        Integer,
        ForeignKey('article.id'),
        nullable=False,
        info={'colanderalchemy': {
            'title': 'id статьи',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    parentRevisionId = Column(
        Integer,
        nullable=True,
        info={'colanderalchemy': {
              'title': 'id предыдущей ревизии',
              'widget': deform.widget.TextInputWidget(readonly=True),
              'typ': NullableInt
        }})

    code = Column(
        Text,
        nullable=False,
        info={'colanderalchemy': {
            'title': 'Код статьи',
            'widget': deform.widget.TextAreaWidget()
        }})

    authorId = Column(
        Integer,
        ForeignKey('user_.id'),
        nullable=False,
        info={'colanderalchemy': {
            'title': 'id автора',
            'widget': deform.widget.TextInputWidget(readonly=True)
        }})

    dateTime = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False,
        info={'colanderalchemy': {
            'title': 'Время создания',
            'widget': deform.widget.DateTimeInputWidget(readonly=True)
        }})

    # relations
    article = relationship("Article", back_populates='revisions')
    author = relationship("User")

    @staticmethod
    def by_id(article_revision_id: int, article_id: int = None):
        """
        :return ArticleRevision
        """
        q = DBSession.query(ArticleRevision).filter(ArticleRevision.id == article_revision_id)
        if article_id is not None:
            q = q.filter(ArticleRevision.articleId == article_id)
        return q.first()

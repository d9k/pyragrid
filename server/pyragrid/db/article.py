from sqlalchemy import (
     Column, Integer, Text, Boolean, DateTime, ForeignKey
)
import deform.widget
import colander
from .base import (Base, DBSession, NullableInt)
from sqlalchemy.orm import (
    Query, relationship
)


class Article(Base):
    __tablename__ = 'Article'

    id = Column(Integer, primary_key=True,
                info={'colanderalchemy': {
                    'title': 'id статьи',
                    'widget': deform.widget.TextInputWidget(readonly=True)
                }})
    name = Column(Text,
                  info={'colanderalchemy': {
                      'title': 'Название статьи',
                      'missing': None,
                  }})
    systemName = Column(Text,
                        nullable=False,
                        unique=True,
                        info={'colanderalchemy': {
                            'title': 'Системное имя',
                            'description': '(index для главной страницы)',
                            'validator': colander.Regex(
                                    '^[a-z0-9_\-/]+$',
                                    'Логин должен содержать только цифры и английские буквы'
                            ),
                            'missing': colander.required
                        }})
    path = Column(Text,
                  unique=True,
                  info={'colanderalchemy': {
                      'title': 'Путь к статье',
                      # TODO description to validator
                      'description': '(должен начинаться с /)',
                      'validator': colander.Regex(
                              '^[a-z0-9_\-/]+$',
                              'Путь должен содержать только цифры и английские буквы'
                      ),
                      # 'missing': colander.required
                  }})
    activeRevisionId = Column(Integer,
                              nullable=True,
                              info={'colanderalchemy': {
                                  'title': 'id активной ревизии',
                                  'widget': deform.widget.TextInputWidget(readonly=True),
                                  'typ': NullableInt
                              }})
    active = Column(Boolean, default=True, server_default='true',
                        nullable=False,
                        info={'colanderalchemy': {
                            'title': 'Статья активна',
                        }})
    isTemplate = Column(Boolean, default=False, server_default='false',
                        nullable=False,
                        info={'colanderalchemy': {
                            'title': 'Является шаблоном',
                        }})

    # relations
    revisions = relationship('ArticleRevision', back_populates='article')

    @staticmethod
    def by_id(article_id: int):
        """
        :return Article
        """
        return DBSession.query(Article).filter(Article.id == article_id).first()

    @staticmethod
    def by_system_name(article_system_name: str, not_id: int = None):
        """
        :return Article
        """
        q = DBSession.query(Article) \
            .filter(Article.systemName == article_system_name)
        q = Article.filter_not_id(q, not_id)
        return q.first()

    @staticmethod
    def by_path(path: str, not_id: int = None):
        """
        :return Article
        """
        if path is None or path == '' or path == colander.null:
            return None
        q = DBSession.query(Article) \
            .filter(Article.path == path)
        q = Article.filter_not_id(q, not_id)
        return q.first()

    @staticmethod
    def filter_not_id(query: Query, not_id):
        if not_id is not None:
            return query.filter(Article.id != not_id)
        return query


class ArticleCustomRoutePredicate:

    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'article custom predicate = ' % [self.val, ]

    phash = text

    def __call__(self, context, request):
        # TODO
        return False

import uuid

from hashlib import sha256
from pyramid.security import (
    Allow
)
from sqlalchemy import (
    BigInteger, Column, Integer, Text, Boolean, DateTime, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session, sessionmaker, Query, relationship
)
import sqlalchemy.event
from zope.sqlalchemy import ZopeTransactionExtension
import deform.widget
import colander
from colander import null, Invalid
from dictalchemy import DictableModel
import dictalchemy.utils
from pyragrid import helpers
import transaction
from sqlalchemy.exc import DBAPIError
import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(), expire_on_commit=False))
""":type: sqlalchemy.orm.Session """

Base = declarative_base(cls=DictableModel)

ADMIN_GROUP = 'admin'
GROUPS = {ADMIN_GROUP: ['group:admins'],
          None: ['group:users']}


class RootFactory(object):
    __acl__ = [(Allow, 'group:users', 'view'),
               (Allow, 'group:admins', ['view', 'admin'])]

    def __init__(self, request):
        pass


def db_save_model(obj):
    try:
        with transaction.manager:
            DBSession.add(obj)
    except DBAPIError as db_api_error:
        return db_api_error
    return None



def create_hashed_password(password, salt):
    return sha256(salt.encode() + password.encode()).hexdigest()


def create_salt():
    return uuid.uuid4().hex


# @colander.deferred
# def email_validator(node, kwargs):
#     return colander.All(
#         colander.Email(),
#         email_unique_validator
#     )


def nullable_int(self, value):
    if value == colander.null or value is None:
        return ''
    else:
        return int(value)


class NullableInt(colander.Number):
    num = nullable_int


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,
                info={'colanderalchemy': {
                    'title': 'id пользователя'
                }})
    vk_id = Column(BigInteger,
                   unique=True,
                   nullable=True,
                   info={'colanderalchemy': {
                       'title': 'id вконтакте',
                       # 'widget': deform.widget.TextInputWidget(),
                       # 'missing': colander.drop,
                       # 'missing': colander.null,
                       # 'default': colander.null,
                       'default': None,
                       'typ': NullableInt
                   }})
    login = Column(Text,
                   unique=True,
                   info={'colanderalchemy': {
                       'title': 'Логин пользователя',
                       'validator': colander.Regex(
                               '^[a-z0-9_]+$',
                               'Логин должен содержать только цифры и английские буквы'
                       ),
                       'missing': colander.required
                   }})
    name = Column(Text,
                  info={'colanderalchemy': {
                      'title': 'Имя пользователя',
                      'missing': None,
                  }})
    email = Column(Text,
                   info={'colanderalchemy': {
                       'title': 'E-mail',
                       'validator': colander.Email(),
                       'missing': colander.required
                       # 'widget': deform.widget.CheckedInputWidget(
                       #     subject='E-mail',
                       #     confirm_subject='Подтвердите E-mail'
                       # )
                   }})
    group = Column(Text,
                   info={'colanderalchemy': {
                       'title': 'Группа пользователя'
                   }})
    email_check_code = Column(Text)
    email_checked = Column(Boolean, default=False, server_default='false', nullable=False,
                           info={'colanderalchemy': {
                               'title': 'Почта проверена'
                           }})
    active = Column(Boolean, default=False, server_default='false', nullable=False,
                    info={'colanderalchemy': {
                        'title': 'Аккаунт включен'
                    }})
    # stores password hash and salt separated by colon
    password_hash = Column(Text, info={'colanderalchemy': {
        'title': 'Пароль',
        'widget': deform.widget.CheckedPasswordWidget(),
    }})

    def set_password(self, password):
        """thx 2 http://pythoncentral.io/hashing-strings-with-python"""
        salt = create_salt()
        self.password_hash = create_hashed_password(password, salt) + ':' + salt

    def check_password(self, user_password):
        if self.password_hash is None:
            return False
        hashed_password_only, salt = self.password_hash.split(':')
        return hashed_password_only == create_hashed_password(user_password, salt)

    @staticmethod
    def get_groups(user_id, request):
        user = User.by_id(user_id)
        """:type user:User"""
        if not user:
            return []
        if user.group not in GROUPS:
            return []
        return GROUPS[user.group]

    @staticmethod
    def by_id(user_id: int):
        """
        :return User
        """
        return DBSession.query(User).filter(User.id == user_id).first()

    @staticmethod
    # def by_login(user_login: str, filters=None):
    def by_login(user_login: str, not_id: int = None):
        """
        :return User
        """
        q = DBSession.query(User) \
            .filter(User.login == user_login)
        q = User.filter_not_id(q, not_id)
        return q.first()

    @staticmethod
    def by_vk_id(vk_id: int):
        """
        :return User
        """
        return DBSession.query(User).filter(User.vk_id == vk_id).first()

    @staticmethod
    def by_email(email: str, not_id: int = None):
        """
        :return User
        """
        q = DBSession.query(User).filter(User.email == email)
        q = User.filter_not_id(q, not_id)
        return q.first()

    @staticmethod
    def filter_not_id(query: Query, not_id):
        if not_id is not None:
            return query.filter(User.id != not_id)
        return query

    @staticmethod
    def by_any(any):
        """
        :return User
        """
        if isinstance(any, int):
            user = User.by_vk_id(any)
            if user:
                return user
        else:
            user = User.by_login(any)
            if user:
                return user

            user = User.by_email(any)
            if user:
                return user

        return None

    @staticmethod
    def generate_password():
        length = int(helpers.get_setting('generate_password_length', 8))
        return helpers.generate_password(length)

    @staticmethod
    def generate_email_check_code():
        length = int(helpers.get_setting('generate_email_check_code_length', 10))
        return helpers.generate_password(length, True)

    def initiate_email_check(self):
        self.email_check_code = self.generate_email_check_code()
        helpers.send_html_mail(self.email, 'email_check_code',
                               {'email_check_code': self.email_check_code})
        self.email_checked = False
        self.active = False

    def is_admin(self):
        return self.group == ADMIN_GROUP

    def before_save(self):
        if not self.name:
            self.name = self.login

# TODO коррекция полей перед сохраненинем
# http://docs.sqlalchemy.org/en/latest/orm/events.html ?
# http://docs.sqlalchemy.org/en/latest/orm/session_events.html


@sqlalchemy.event.listens_for(User, 'before_insert')
def user_before_insert(mapper, connection, user: User):
    user.before_save()


@sqlalchemy.event.listens_for(User, 'before_update')
def user_before_update(mapper, connection, user: User):
    user.before_save()


class Article(Base):
    __tablename__ = 'articles'

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
                        info={'colanderalchemy': {
                            'title': 'Системное имя',
                            'validator': colander.Regex(
                                    '^[a-z0-9_\-/]+$',
                                    'Логин должен содержать только цифры и английские буквы'
                            ),
                            'missing': colander.required
                        }})
    path = Column(Text,
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
    def by_system_name(article_system_name: str):
        """
        :return Article
        """
        return DBSession.query(Article).filter(Article.systemName == article_system_name).first()

    @staticmethod
    def by_path(path: str):
        """
        :return Article
        """
        if path is None or path == '':
            return None
        return DBSession.query(Article).filter(Article.path == path).first()


class ArticleRevision(Base):
    __tablename__ = 'articles_revisions'
    id = Column(Integer, primary_key=True,
                info={'colanderalchemy': {
                    'title': 'глобальный id ревизии',
                    'widget': deform.widget.TextInputWidget(readonly=True)
                }})
    articleId = Column(Integer,
                       ForeignKey('articles.id'),
                       nullable=False,
                       info={'colanderalchemy': {
                           'title': 'id статьи',
                           'widget': deform.widget.TextInputWidget(readonly=True)
                       }})
    parentRevisionId = Column(Integer,
                              nullable=True,
                              info={'colanderalchemy': {
                                    'title': 'id предыдущей ревизии',
                                    'widget': deform.widget.TextInputWidget(readonly=True),
                                    'typ': NullableInt
                              }})
    code = Column(Text,
                  nullable=False,
                  info={'colanderalchemy': {
                      'title': 'Код статьи',
                      'widget': deform.widget.TextAreaWidget()
                  }})
    authorId = Column(Integer,
                      ForeignKey('users.id'),
                      nullable=False,
                      info={'colanderalchemy': {
                          'title': 'id автора',
                          'widget': deform.widget.TextInputWidget(readonly=True)
                      }})
    dateTime = Column(DateTime,
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


class ArticleCustomRoutePredicate:

    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'article custom predicate = ' % [self.val, ]

    phash = text

    def __call__(self, context, request):
        # TODO
        return False


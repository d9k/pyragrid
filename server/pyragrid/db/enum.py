from .. import helpers

# from sqlalchemy.types import SchemaType, TypeDecorator, Enum
# import re

# thx http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/


# class EnumSymbol(object):
#     """Define a fixed symbol tied to a parent class."""
#
#     def __init__(self, cls_, name, value, description):
#         self.cls_ = cls_
#         self.name = name
#         self.value = value
#         self.description = description
#
#     def __reduce__(self):
#         """Allow unpickling to return the symbol
#         linked to the DeclEnum class."""
#         return getattr, (self.cls_, self.name)
#
#     def __iter__(self):
#         return iter([self.value, self.description])
#
#     def __repr__(self):
#         return "<%s>" % self.name
#
#
# class EnumMeta(type):
#     """Generate new DeclEnum classes."""
#
#     def __init__(cls, classname, bases, dict_):
#         cls._reg = reg = cls._reg.copy()
#         for k, v in list(dict_.items()):
#             if isinstance(v, tuple):
#                 sym = reg[v[0]] = EnumSymbol(cls, k, *v)
#                 setattr(cls, k, sym)
#         # return type.__init__(cls, classname, bases, dict_)
#         type.__init__(cls, classname, bases, dict_)
#
#     def __iter__(cls):
#         return iter(list(cls._reg.values()))
#
#
# class DeclEnum(object, metaclass=EnumMeta):
#     """Declarative enumeration."""
#     _reg = {}
#
#     @classmethod
#     def from_string(cls, value):
#         try:
#             return cls._reg[value]
#         except KeyError:
#             raise ValueError(
#                     "Invalid value for %r: %r" %
#                     (cls.__name__, value)
#                 )
#
#     @classmethod
#     def values(cls):
#         return list(cls._reg.keys())
#
#     @classmethod
#     def db_type(cls):
#         return DeclEnumType(cls)
#
#
# class DeclEnumType(SchemaType, TypeDecorator):
#     def __init__(self, enum):
#         self.enum = enum
#         self.impl = Enum(
#                         *list(enum.values()),
#                         name="ck%s" % re.sub(
#                                     '([A-Z])',
#                                     lambda m:"_" + m.group(1).lower(),
#                                     enum.__name__)
#                     )
#
#     def _set_table(self, table, column):
#         self.impl._set_table(table, column)
#
#     def copy(self):
#         return DeclEnumType(self.enum)
#
#     def process_bind_param(self, value, dialect):
#         if value is None:
#             return None
#         return value.value
#
#     def process_result_value(self, value, dialect):
#         if value is None:
#             return None
#         return self.enum.from_string(value.strip())


class SimpleEnumMeta(type):
    def __init__(_class, name, bases, dic: dict):
        _class._values = []
        _class._descriptions = {}
        for property_name in dic.keys():
            if property_name.startswith('_'):
                continue
            value = dic[property_name]
            description = ''
            if type(value) is classmethod:
                continue
            if type(value) is tuple:
                description = helpers.tuple_get(value, 1, '')
                value = helpers.tuple_get(value, 0, '')
            if value == '':
                value = property_name
            if description == '':
                description = property_name
            setattr(_class, property_name, value)
            _class._values.append(getattr(_class, property_name))
            _class._descriptions[value] = description

        super().__init__(name, bases, dic)


class SimpleEnum(object, metaclass=SimpleEnumMeta):
    """if the value of class field is '' (empty string), value of this field would be the same as fields name"""

    @classmethod
    def get_values(_class):
        return _class._values

    @classmethod
    def get_descriptions(_class):
        return _class._descriptions



import unittest
import transaction

from pyramid import testing

from pyragrid import helpers


class MyUnitTest(unittest.TestCase):
    def setUp(self):
        self.request = testing.DummyRequest()
        self.config = testing.setUp()

    def test_build_url(self):

        self.assertEqual(
            'http://example.com/test.html',
            helpers.build_url('http://example.com/test.html', {})
        )
        self.assertIn(
            helpers.build_url('http://example.com/test.html', {'param1': 'some words', 'param2': '', 'param3': '3'}),
            # WTF with order?
            ['http://example.com/test.html?param1=some+words&param2=&param3=3',
             'http://example.com/test.html?param1=some+words&param3=3&param2=',
             'http://example.com/test.html?param2=&param1=some+words&param3=3',
             'http://example.com/test.html?param2=&param3=3&param1=some+words',
             'http://example.com/test.html?param3=3&param1=some+words&param2=',
             'http://example.com/test.html?param3=3&param2=&param1=some+words']
        )

    def test_dict_has_keys(self):
        has_keys = helpers.dict_has_keys
        T = self.assertTrue
        F = self.assertFalse
        T(has_keys({'a': 1, 'b': 2, 'd': 3}, []))
        T(has_keys({'a': 1, 'b': 2, 'd': 3}, ['a']))
        T(has_keys({'a': 1, 'b': 2, 'd': 3}, ['a', 'b']))
        T(has_keys({'a': 1, 'b': 2, 'd': 3}, ['a', 'b', 'd']))
        F(has_keys({'a': 1, 'b': 2, 'd': 3}, ['c']))
        F(has_keys({'a': 1, 'b': 2, 'd': 3}, ['a', 'b', 'c', 'd']))

    def test_dict_has_data(self):
        has_data = helpers.dict_has_data
        T = self.assertTrue
        F = self.assertFalse
        T(has_data({'a': 1, 'b': 2, 'd': 3}, {}))
        T(has_data({'a': 1, 'b': 2, 'd': 3}, {'a': 1}))
        T(has_data({'a': 1, 'b': 2, 'd': 3}, {'a': 1, 'b': 2}))
        F(has_data({'a': 1, 'b': 2, 'd': 3}, {'a': 1, 'b': -1}))
        F(has_data({'a': 1, 'b': 2, 'd': 3}, {'a': 1, 'b': 2, 'c': 0}))
        F(has_data({'a': 1, 'b': 2, 'd': 3}, {'c': 0}))
        F(has_data({'a': 1, 'b': 2, 'd': 3}, {'a': 1, 'b': 2, 'c': 0, 'd': 3}))

    def test_dict_to_vars(self):
        to_vars = helpers.dict_to_vars
        eq = self.assertEqual
        a, b, d = to_vars({'a': 1, 'b': 2, 'c': 3, 'd': 4}, ['a', 'b', 'd'])
        eq(a, 1); eq(b, 2); eq(d, 4)
        del a, b, d

        def test_key_error():
            a, b, e = to_vars({'a': 1, 'b': 2, 'c': 3, 'd': 4}, ['a', 'b', 'e'])

        self.assertRaises(KeyError, test_key_error)

    def tearDown(self):
        testing.tearDown()

# class TestMyViewSuccessCondition(unittest.TestCase):
#     def setUp(self):
#         self.config = testing.setUp()
#         from sqlalchemy import create_engine
#         engine = create_engine('sqlite://')
#         from .models__ import (
#             Base,
#             MyModel,
#             )
#         DBSession.configure(bind=engine)
#         Base.metadata.create_all(engine)
#         with transaction.manager:
#             model = MyModel(name='one', value=55)
#             DBSession.add(model)
#
#     def tearDown(self):
#         DBSession.remove()
#         testing.tearDown()
#
#     def test_passing_view(self):
#         from .views import my_view
#         request = testing.DummyRequest()
#         info = my_view(request)
#         self.assertEqual(info['one'].name, 'one')
#         self.assertEqual(info['project'], 'pyragrid')
#
#
# class TestMyViewFailureCondition(unittest.TestCase):
#     def setUp(self):
#         self.config = testing.setUp()
#         from sqlalchemy import create_engine
#         engine = create_engine('sqlite://')
#         from .models__ import (
#             Base,
#             MyModel,
#             )
#         DBSession.configure(bind=engine)
#
#     def tearDown(self):
#         DBSession.remove()
#         testing.tearDown()
#
#     def test_failing_view(self):
#         from .views import my_view
#         request = testing.DummyRequest()
#         info = my_view(request)
#         self.assertEqual(info.status_int, 500)

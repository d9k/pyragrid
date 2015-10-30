import unittest
import transaction

from pyramid import testing


class MyUnitTest(unittest.TestCase):
    def setUp(self):
        self.request = testing.DummyRequest()
        self.config = testing.setUp()

    def test_build_url(self):
        from best_tests_server import helpers

        self.assertEqual(
            'http://example.com/test.html',
            helpers.build_url('http://example.com/test.html', {})
        )
        self.assertIn(
            helpers.build_url('http://example.com/test.html', {'param1': 'some words', 'param2': '', 'param3': '3'}),
            # WTF with order?
            ['http://example.com/test.html?param3=3&param1=some+words&param2=',
             'http://example.com/test.html?param3=3&param2=&param1=some+words']
        )

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
#         self.assertEqual(info['project'], 'best_tests_server')
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

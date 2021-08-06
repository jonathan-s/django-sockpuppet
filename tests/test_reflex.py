from django.test import TestCase
from sockpuppet.test_utils import reflex_factory
from sockpuppet.reflex import Context


class ReflexTests(TestCase):

    def test_reflex_can_access_context(self):
        reflex = reflex_factory('/test/', self.client)
        context = reflex.get_context_data()

        self.assertIn('count', context)
        self.assertIn('otherCount', context)

    def test_context_api_works_correctly(self):
        '''Test that context correctly stores information'''
        context = Context()
        context.hello = 'hello'

        self.assertEqual(context.hello, 'hello')
        self.assertEqual(context['hello'], 'hello')

        with self.assertRaises(AttributeError):
            context.not_an_attribute

        with self.assertRaises(KeyError):
            context['not_in_dictionary']

    def test_access_attribute_when_stored_as_dict(self):
        '''When value stored as dictionary it should be accessible as attribute'''
        context = Context()
        context['hello'] = 'world'
        print(context.__dict__)
        self.assertEqual(context['hello'], 'world')
        self.assertEqual(context.hello, 'world')

    def test_update_context(self):
        '''Update context with normal dictionary'''

        context = Context()
        # update is broken.
        context.update({'hello': 'world'})
        self.assertEqual(context.hello, 'world')

    def test_context_contains_none(self):
        context = Context()
        context.none = None
        self.assertEqual(context.none, None)
        self.assertEqual(context['none'], None)

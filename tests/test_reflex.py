from django.test import TestCase
from sockpuppet.test_utils import reflex_factory


class ReflexTests(TestCase):

    def test_reflex_can_access_context(self):
        reflex = reflex_factory('/test/', self.client)
        context = reflex.get_context_data()

        self.assertIn('count', context)
        self.assertIn('otherCount', context)

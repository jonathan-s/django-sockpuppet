from django.test import TestCase

from sockpuppet.templatetags.sockpuppet import camelcase, pascalcase


class CamelcaseFilterTest(TestCase):
    def test_camelcase(self):
        self.assertEqual(camelcase("foo"), "foo")

    def test_double_camelcase(self):
        self.assertEqual(camelcase("foo_bar"), "fooBar")

    def test_triple_camelcase(self):
        self.assertEqual(camelcase("foo_bar_baz"), "fooBarBaz")

    def test_reverse_camelcase(self):
        self.assertEqual(camelcase("Foo"), "foo")

    def test_wild_camelcase(self):
        self.assertEqual(camelcase("FooBarBaz"), "foobarbaz")

    def test_wild_camelcase_with_CAPITALS(self):
        self.assertEqual(camelcase("FooBARBaz"), "foobarbaz")

    def test_wild_double_camelcase(self):
        self.assertEqual(camelcase("FooBarBaz_FooBarBaz"), "foobarbazFoobarbaz")

    def test_double_reverse_camelcase(self):
        self.assertEqual(camelcase("Foo_bar"), "fooBar")


class PascalcaseFilterTest(TestCase):
    def test_pascalcase(self):
        self.assertEqual(pascalcase("foo"), "Foo")

    def test_double_pascalcase(self):
        self.assertEqual(pascalcase("foo_bar"), "FooBar")

    def test_triple_pascalcase(self):
        self.assertEqual(pascalcase("foo_bar_baz"), "FooBarBaz")

    def test_reverse_pascalcase(self):
        self.assertEqual(pascalcase("Foo"), "Foo")

    def test_wild_pascalcase(self):
        self.assertEqual(pascalcase("FooBarBaz"), "Foobarbaz")

    def test_wild_pascalcase_with_CAPITALS(self):
        self.assertEqual(pascalcase("FooBARBaz"), "Foobarbaz")

    def test_wild_double_pascalcase(self):
        self.assertEqual(pascalcase("FooBarBaz_FooBarBaz"), "FoobarbazFoobarbaz")

    def test_double_reverse_pascalcase(self):
        self.assertEqual(pascalcase("Foo_bar"), "FooBar")

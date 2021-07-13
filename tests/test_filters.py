from django.test import TestCase

from sockpuppet.templatetags.sockpuppet import camelcase, pascalcase


class CamelcaseFilterTest(TestCase):
    def test_camelcase(self):
        self.assertEqual(camelcase("Foo"), "foo")

    def test_2_camelcase(self):
        self.assertEqual(camelcase("foo_bar"), "fooBar")

    def test_3_camelcase(self):
        self.assertEqual(camelcase("foo_bar_baz"), "fooBarBaz")

    def test_preserve_already_camelcase(self):
        self.assertEqual(camelcase("foo"), "foo")

    def test_preserve_already_3_camelcase(self):
        self.assertEqual(camelcase("fooBarBaz"), "fooBarBaz")

    def test_pascalcase2camelcase(self):
        self.assertEqual(camelcase("FooBarBaz"), "fooBarBaz")

    def test_correct_CAPITALS_camelcase(self):
        self.assertEqual(camelcase("test_GUI_part"), "testGuiPart")

    def test_2_mixed_camelcase(self):
        self.assertEqual(camelcase("FooBarBaz_FooBarBaz"), "foobarbazFoobarbaz")

    def test_2_reverse_camelcase(self):
        self.assertEqual(camelcase("Foo_bar"), "fooBar")

    def test_double_camelcase(self):
        self.assertEqual(camelcase(camelcase("foo_bar")), "fooBar")


class PascalcaseFilterTest(TestCase):
    def test_pascalcase(self):
        self.assertEqual(pascalcase("foo"), "Foo")

    def test_2_pascalcase(self):
        self.assertEqual(pascalcase("foo_bar"), "FooBar")

    def test_3_pascalcase(self):
        self.assertEqual(pascalcase("foo_bar_baz"), "FooBarBaz")

    def test_preserve_already_pascalcase(self):
        self.assertEqual(pascalcase("FooBar"), "FooBar")

    def test_preserve_already_3_pascalcase(self):
        self.assertEqual(pascalcase("FooBarBaz"), "FooBarBaz")

    def test_camelcase2pascalcase(self):
        self.assertEqual(pascalcase("fooBarBaz"), "FooBarBaz")

    def test_correct_CAPITALS_pascalcase(self):
        self.assertEqual(pascalcase("test_GUI_part"), "TestGuiPart")

    def test_2_mixed_pascalcase(self):
        self.assertEqual(pascalcase("FooBarBaz_FooBarBaz"), "FoobarbazFoobarbaz")

    def test_2_reverse_pascalcase(self):
        self.assertEqual(pascalcase("foo_Bar"), "FooBar")

    def test_double_pascalcase(self):
        self.assertEqual(pascalcase(pascalcase("foo_bar")), "FooBar")

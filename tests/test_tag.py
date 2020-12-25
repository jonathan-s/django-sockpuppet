from django.template.response import TemplateResponse
from django.test import TestCase, Client


class TestTagSupport(TestCase):

    def test_reflex_tag(self):
        c = Client()
        response: TemplateResponse = c.get('/tag/')

        content = response.content.decode('utf-8')

        self.assertEqual('\n<a href="#" data-reflex="click->example_reflex#increment" data-parameter="I am a parameter">click me</a>\n', content)

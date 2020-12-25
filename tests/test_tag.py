from django.template.response import TemplateResponse
from django.test import TestCase, Client


class TestTagSupport(TestCase):

    def test_click_reflex_tag(self):
        c = Client()
        response: TemplateResponse = c.get('/tag/')

        content = response.content.decode('utf-8')

        self.assertTrue(content.__contains__('<a href="#" data-reflex="click->example_reflex#increment" '
                                             'data-parameter="I am a parameter">'
                                             'click me'
                                             '</a>'))

    def test_submit_reflex_tag(self):
        c = Client()
        response: TemplateResponse = c.get('/tag/')

        content = response.content.decode('utf-8')

        self.assertTrue(content.__contains__('<a href="#" data-reflex="submit->example_reflex#increment" '
                                             'data-parameter="I am a parameter">'
                                             'click me'
                                             '</a>'))

    def test_input_reflex_tag(self):
        c = Client()
        response: TemplateResponse = c.get('/tag/')

        content = response.content.decode('utf-8')

        self.assertTrue(content.__contains__(
            '<input type="text" data-reflex="input->example_reflex#increment" data-parameter="I am a parameter"/>'))

    def test_reflex_tag_with_unsafe_input(self):
        c = Client()
        response: TemplateResponse = c.get('/tag/', data={"parameter": "</a>"})

        content = response.content.decode('utf-8')

        self.assertTrue(content.__contains__('<a href="#" data-reflex="click->example_reflex#increment" '
                                             'data-parameter="&lt;/a&gt;">'
                                             'click me'
                                             '</a>'))

    def test_controller_tag(self):
        c = Client()
        response: TemplateResponse = c.get('/second/', data={"parameter": "</a>"})

        content = response.content.decode('utf-8')

        self.assertTrue(content.__contains__(
            '<a href="#" data-reflex="click->example_reflex#increment" data-parameter="&lt;/a&gt;" data-param2="abc">click me</a>'))

    def test_tag_by_dict(self):
        c = Client()
        response: TemplateResponse = c.get('/second/', data={"parameter": "</a>"})

        content = response.content.decode('utf-8')

        print(content)

        self.assertTrue(content.__contains__(
            '<a href="#" data-reflex="click->abc#increment" >I was done by object definition</a>'))

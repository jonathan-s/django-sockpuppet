from django.template.loader import render_to_string
from django.template.backends.django import Template
from django.test import RequestFactory

from .channel import Channel

PROTECTED_VARIABLES = [
    'consumer',
    'element',
    'is_morph',
    'selectors',
    'session',
    'url',
]


class Reflex:
    def __init__(
        self, consumer, url, element, selectors, params, identifier='',
        permanent_attribute_name=None, reflex_id=None
    ):
        self.consumer = consumer
        self.url = url
        self.element = element
        self.selectors = selectors
        self.session = consumer.scope['session']
        self.params = params
        self.identifier = identifier
        self.is_morph = False
        self.reflex_id = reflex_id
        self.permanent_attribute_name = permanent_attribute_name

    @property
    def request(self):
        factory = RequestFactory()
        request = factory.get(self.url)
        request.session = self.consumer.scope['session']
        request.user = self.consumer.scope['user']
        request.POST = self.params
        return request

    def reload(self):
        """A default reflex to force a refresh"""
        pass

    def get_channel_id(self):
        '''
        Override this to make the reflex send to a different channel
        other than the session_key of the user
        '''
        return self.session.session_key

    def morph(self, selector='', html='', template='', context={}):
        """
        If a morph is executed without any arguments, nothing is executed
        and the reflex won't send over any data to the frontend.
        """
        self.is_morph = True
        no_arguments = [not selector, not html, (not template and not context)]
        if all(no_arguments) and not selector:
            # an empty morph, nothing is sent ever.
            return

        if html:
            html = html
        elif isinstance(template, Template):
            html = template.render(context)
        else:
            html = render_to_string(template, context)

        broadcaster = Channel(self.get_channel_id(), identifier=self.identifier)
        broadcaster.morph({
            'selector': selector,
            'html': html,
            'children_only': True,
            'permanent_attribute_name': self.permanent_attribute_name,
            'stimulus_reflex': {
                'morph': 'selector',
                'reflexId': self.reflex_id,
                'url': self.url
            }
        })
        broadcaster.broadcast()

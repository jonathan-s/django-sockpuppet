from django.urls import resolve
from urllib.parse import urlparse

from django.test import RequestFactory

PROTECTED_VARIABLES = [
    'consumer',
    'element',
    'selectors',
    'session',
    'url',
]


class Reflex:
    def __init__(self, consumer, url, element, selectors, params):
        self.consumer = consumer
        self.url = url
        self.element = element
        self.selectors = selectors
        self.session = consumer.scope['session']
        self.params = params
        self.context = {}

    def __repr__(self):
        return f'<Reflex url: {self.url}, session: {self.get_channel_id()}>'

    def get_context_data(self, *args, **kwargs):
        if self.context:
            self.context.update(**kwargs)
            return self.context

        parsed_url = urlparse(self.url)
        resolved = resolve(parsed_url.path)
        view = resolved.func.view_class()
        view.request = self.request
        try:
            context = view.get_context_data()
        except AttributeError:
            view.get(self.request)
            context = view.get_context_data()

        self.context = context
        self.context.update(**kwargs)
        return self.context

    def get_channel_id(self):
        '''
        Override this to make the reflex send to a different channel
        other than the session_key of the user
        '''
        return self.session.session_key

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

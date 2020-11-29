from django.test import RequestFactory

PROTECTED_VARIABLES = [
    'consumer',
    'element',
    'selectors',
    'session',
    'url',
]


class Reflex:
    def __init__(self, consumer, url, element, selectors):
        self.consumer = consumer
        self.url = url
        self.element = element
        self.selectors = selectors
        self.session = consumer.scope['session']

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
        return request

    def reload(self):
        """A default reflex to force a refresh"""
        pass
